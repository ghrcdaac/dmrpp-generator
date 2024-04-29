variable "region" {
  type    = string
  default = "us-west-2"
}

variable "account_id" {
  type = string
}

variable "prefix" {
  type        = string
  description = "Cumulus stack prefix"
}

variable "cumulus_lambda_role_arn" {
  type = string
  default = ""
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

variable "docker_image" {
    description = "ECR Lambda docker image"
    type    = string
    default = "ghrcdaac/dmrpp-generator:VERSION_SUB"
}
