variable "aws_profile" {
  type    = string
  default = null
}


variable "region" {
  type    = string
  default = "us-west-2"
}


variable "prefix" {
  type = string
  description = "Cumulus stack prefix"
}

variable "desired_count" {
  default = 1
}
variable "cpu" {
  default = 800
}

variable "memory_reservation" {
  default = 900
}
variable "cluster_arn" {}
variable "log2elasticsearch_lambda_function_arn" {}
variable "environement" {
  default = {
    AWS_DEFAULT_REGION = "us-west-2"
  }
}
variable "docker_image" {
  default = "ghrcdaac/dmrpp-generator:latest"
}
