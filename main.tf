module "dmrpp_service" {
  source              = "./modules/dmrpp_service"
  prefix              = var.prefix
  cluster_arn         = var.cluster_arn
  desired_count       = var.desired_count
  log_destination_arn = var.log_destination_arn
  docker_image        = var.docker_image
  cpu                 = var.cpu
  memory_reservation  = var.memory_reservation
  region              = var.region
  volumes             = var.volumes
  enable_cw_logging   = var.enable_cw_logging
  get_dmrpp_timeout   = var.get_dmrpp_timeout
}

module "dmrpp_lambda" {
  source = "./modules/dmrpp_lambda"

  region = var.region
  prefix = var.prefix
  docker_image = var.docker_image
  enable_cw_logging  = var.enable_cw_logging
  get_dmrpp_timeout  = var.get_dmrpp_timeout
  cumulus_lambda_role_arn = var.cumulus_lambda_role_arn
}
