output "dmrpp_lambda_arn" {
  value = join("", aws_lambda_function.dmrpp_generator.*.arn)
}