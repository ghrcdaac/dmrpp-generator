variable "prefix" {}
variable "default_tags" {}
variable "desired_count" {}
variable "cpu" {}
variable "memory_reservation" {}
variable "region" {}
variable "cluster_arn" {}
variable "log2elasticsearch_lambda_function_arn" {}
variable "docker_image" {}
variable "environement" {
  type = object({})
  description = "Environement variables passed to DMP++ service"
}