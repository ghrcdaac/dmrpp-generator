
#!/bin/bash
set -o errexit
set -o nounset
set -o pipefail
export REPO_NAME=ghrcw-dmrpp-generator-lambda
export SERVICE_NAME=dmrpp_generator
export AWS_REGION=$bamboo_AWS_REGION


access_keys=( $bamboo_AWS_PROD_ACCESS_KEY )
secret_keys=( $bamboo_AWS_PROD_SECRET_ACCESS_KEY )
prefixes=( $bamboo_PREFIX_PROD )
account_numbers=( $bamboo_ACCOUNT_NUMBER_PROD )


function stop_ecs_task() {
  task_arns=$(aws ecs list-tasks --cluster $1-CumulusECSCluster --family $1-$2 --query "taskArns[*]" --region $AWS_REGION | tr -d '"[],')
  for task in $task_arns
  do
    aws ecs stop-task --cluster $1-CumulusECSCluster --task $task --region $AWS_REGION
  done
}


function push_to_ecr() {
  # $ACCOUNT_NUMBER = $1
  # $prefix = $2
  docker_image_name=$1.dkr.ecr.$AWS_REGION.amazonaws.com/$REPO_NAME:$bamboo_TagBuildTriggerReason_tagName
  docker tag $REPO_NAME $docker_image_name

  echo "ECR login"
  aws ecr get-login-password \
      --region $AWS_REGION \
  | docker login \
      --username AWS \
      --password-stdin $1.dkr.ecr.$AWS_REGION.amazonaws.com

  #aws ecr create-repository --repository-name $REPO_NAME 2> /dev/null
  echo "pushing image to ecr"
  docker push $docker_image_name

  # stop_ecs_task $2 $SERVICE_NAME

  docker rmi $docker_image_name
}


function build_docker {
echo $bamboo_GITHUB_REGISTRY_READ_TOKEN_SECRET | docker login ghcr.io -u bamboo_login --password-stdin
if [[ $(uname -m) == arm64* ]]; then
  docker_build="docker buildx build --push --platform linux/arm64,linux/amd64 -t"
else
 docker_build="docker build -t"
fi
${docker_build} $1 .

}


len=${#access_keys[@]}

# Check keys are valid
for (( i=0; i<$len; i++ ))
do
  export AWS_ACCESS_KEY_ID=${access_keys[$i]}
  export AWS_SECRET_ACCESS_KEY=${secret_keys[$i]}
  aws sts get-caller-identity
  (($? != 0)) && { printf '%s\n' "Command exited with non-zero. AWS keys invalid"; exit 1; }
done


build_docker ${REPO_NAME}
for (( i=0; i<$len; i++ ))
do
  export AWS_ACCESS_KEY_ID=${access_keys[$i]}
  export AWS_SECRET_ACCESS_KEY=${secret_keys[$i]}
  export ACCOUNT_NUMBER=${account_numbers[$i]}
  export prefix=${prefixes[$i]}
  push_to_ecr $ACCOUNT_NUMBER $prefix
done


docker rmi $REPO_NAME
