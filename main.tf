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
  tags = var.default_tags
  cluster_arn                           = var.cluster_arn
  desired_count                         = var.desired_count
  log2elasticsearch_lambda_function_arn = var.log2elasticsearch_lambda_function_arn

  cpu                = var.cpu
  memory_reservation = var.memory_reservation
  environment = var.environement
}
