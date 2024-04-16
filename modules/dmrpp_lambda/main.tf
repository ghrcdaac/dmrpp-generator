resource "aws_lambda_function" "ghrc_dmrpp" {
  function_name = "${var.prefix}-ghrc-dmrpp"
  package_type = "Image"
  image_uri = var.docker_image
  role = var.cumulus_lambda_role_arn
  timeout = var.timeout
  memory_size = var.memory_size

  image_config {
    entry_point = ["/home/worker/miniconda/bin/python", "-m", "awslambdaric"]
    command = ["dmrpp_generator.lambda_handler.handler"]
  }

  ephemeral_storage {
    size = var.ephemeral_storage
  }

  environment {
    variables = {
      region = var.region
      ENABLE_CW_LOGGING = var.enable_cw_logging
      GET_DMRPP_TIMEOUT = var.get_dmrpp_timeout
    }
  }
}