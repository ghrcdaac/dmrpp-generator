variable "prefix" {}
variable "desired_count" {}
variable "cpu" {}
variable "memory_reservation" {}
variable "region" {}
variable "cluster_arn" {}
variable "log_destination_arn" {}
variable "docker_image" {}
variable "volumes" {}
variable "enable_cw_logging" {}
variable "get_dmrpp_timeout" {}

variable "default_log_retention_days" {
  type = number
  default = 30
  description = "Default value that user chooses for their log retention periods"
}

variable "efs_fs_id" {}
variable "access_point_id" {}