aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 322322076095.dkr.ecr.us-west-2.amazonaws.com && \
docker build -t monolith_testing_dmrpp . && \
docker tag monolith_testing_dmrpp:latest 322322076095.dkr.ecr.us-west-2.amazonaws.com/monolith_testing_dmrpp:latest && \
docker push 322322076095.dkr.ecr.us-west-2.amazonaws.com/monolith_testing_dmrpp:latest