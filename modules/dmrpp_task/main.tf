
locals {
  default_tags = {
    Deployment = var.prefix
  }
}

resource "aws_sfn_activity" "dmrpp_ecs_task" {
  name = var.name
  tags = local.default_tags
}