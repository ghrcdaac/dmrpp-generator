resource "aws_sfn_activity" "dmrpp_ecs_task" {
  name = var.name
  tags = var.tags
}