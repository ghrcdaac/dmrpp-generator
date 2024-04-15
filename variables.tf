variable "aws_profile" {
  type    = string
  default = null
}

variable "region" {
  type    = string
  default = "us-west-2"
}

variable "prefix" {
  type        = string
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
variable "log_destination_arn" {
  type        = string
  default     = null
  description = "A shared AWS:Log:Destination that receives logs in log_groups"
}
variable "docker_image" {
    description = "Docker image used to generate DMRPP"
    type    = string
    default = "ghrcdaac/dmrpp-generator:VERSION_SUB"
}

variable "volumes" {
  description = "Volumes to make accessible to the container(s)"
  type        = list(object({ name = string, host_path = string, container_path = string }))
  default     = []
}

variable "enable_cw_logging" {
  description = "Enable logging to cloud watch"
  type        = bool
  default     = true
}

variable "get_dmrpp_timeout" {
  description = "Duration to wait on the get_dmrpp subprocess call."
  type    = number
  default = 60
}

variable "default_log_retention_days" {
  type = number
  default = 30
  description = "Default value that user chooses for their log retention periods"
}

# Lambda Variables
variable "cumulus_lambda_role_arn" {
  type = string
  nullable = true
}

variable "timeout" {
  description = "Lambda function time-out"
  default     = 900
}

variable "memory_size" {
  description = "Lambda RAM limit"
  default     = 256
}

variable "ephemeral_storage" {
  description = "Lambda /tmp storage limit"
  default     = 512
}
