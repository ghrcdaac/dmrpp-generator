terraform {
  required_providers {
    aws  = ">= 2.31.0"
    null = "~> 2.1"
  }
}

provider "aws" {
  region  = var.region
  profile = var.aws_profile
}


module "dmrpp_service" {
  source = "./modules/dmrpp_service"
  prefix = var.prefix
  cluster_arn                           = var.cluster_arn
  desired_count                         = var.desired_count
  log2elasticsearch_lambda_function_arn = var.log2elasticsearch_lambda_function_arn
  docker_image = var.docker_image
  cpu                = var.cpu
  memory_reservation = var.memory_reservation
}
