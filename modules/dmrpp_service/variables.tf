variable "prefix" {}
variable "desired_count" {}
variable "cpu" {}
variable "memory_reservation" {}
variable "region" {}
variable "cluster_arn" {}
variable "log_destination_arn" {
  type        = string
  default     = null
  description = "A shared AWS:Log:Destination that receives logs in log_groups"
}
variable "docker_image" {}
variable "volumes" {}
