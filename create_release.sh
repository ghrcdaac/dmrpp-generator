#!/bin/bash
set -ex
export VERSION=$1
export RELEASE_NAME=$(basename "$GITHUB_REPO")

## Create Release
 export RELEASE_URL=$(curl -H\
"Authorization: token $GITHUB_TOKEN"\
 -d "{\"tag_name\": \"$VERSION\", \"target_commitsh\": \"$VERSION\", \"name\": \"$VERSION\", \"body\": \"Release $VERSION\" }"\
 -H "Content-Type: application/json"\
 -X POST\
 https://api.github.com/repos/"$GITHUB_REPO"/releases \
 | grep \"url\" | grep releases | sed -e 's/.*\(https.*\)\"\,/\1/' | sed -e 's/api/uploads/')



## Build TF modules that require source building
function create_zip_file() {
  BUILD_DIR=/tmp/${RELEASE_NAME}
  DESTINATION_DIR=${PWD}/dist
  rm -rf "${DESTINATION_DIR}"
  mkdir -p "${BUILD_DIR}" "${DESTINATION_DIR}"
  cp -r modules "${BUILD_DIR}"
  cp -- *tf "${BUILD_DIR}"
  cd "${BUILD_DIR}"
  sed -i "s/VERSION_SUB/${VERSION}/g" variables.tf
  zip -r9 "${RELEASE_NAME}".zip .
  mv "${RELEASE_NAME}".zip "${DESTINATION_DIR}"/.
  cd "$DESTINATION_DIR"
  rm -rf "${BUILD_DIR}"
}

function create_wheel() {
  echo pwd
  python -m build --wheel --outdir . .
}

#### Release package
create_zip_file

### Post the release
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" --data-binary "@${RELEASE_NAME}.zip" \
  -H "Content-type: application/octet-stream" \
  "$RELEASE_URL"/assets?name="${RELEASE_NAME}".zip

### Post the wheel
pwd
ls
content=$(cat ./dmrpp_generator/version.py)
[[ $content =~ ([0-9]+.[0-9]+.[0-9]+) ]]
curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  -H "Content-Type: application/octet-stream" \
  "$RELEASE_URL/assets?name=dmrpp_file_generator-${BASH_REMATCH[1]}-py3-none-any.whl" \
  --data-binary "@example.zip"

## Create Release for dmrpp docker image
#curl -H\
#  "Authorization: token $GITHUB_TOKEN"\
#   -d "{\"tag_name\": \"$VERSION\", \"target_commitsh\": \"$VERSION\", \"name\": \"$VERSION\", \"body\": \"Release $VERSION https://ghrcdaac.github.io/dmrpp-generator\" }"\
#   -H "Content-Type: application/json"\
#   -X POST\
#   https://api.github.com/repos/$GUTHUB_DOCKER_IMAGE/releases
