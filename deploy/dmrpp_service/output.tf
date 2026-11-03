output "dmrpp_service" {
  value = module.dmrpp_service
}

output "dmrpp_task_id" {
  value = module.dmrpp_ecs_task_module.task_id
}