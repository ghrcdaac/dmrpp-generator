terraform {
  required_providers {
    aws  = ">= 2.31.0"
    null = "~> 2.1"
  }
}

module "dmrpp_service" {
  source = "./modules/dmrpp_service"
  prefix = var.prefix
  cluster_arn                           = var.cluster_arn
  desired_count                         = var.desired_count
  log_destination_arn = var.log_destination_arn
  docker_image = var.docker_image
  cpu                = var.cpu
  memory_reservation = var.memory_reservation
  region = var.region
  volumes = var.volumes
}
