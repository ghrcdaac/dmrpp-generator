locals {
  image_version = regex("v\\d+.\\d+.\\d+", var.docker_image)
  deploy_lambda = length(var.cumulus_lambda_role_arn) > 0 ? true : false
}

resource "aws_lambda_function" "ghrc_dmrpp" {
  count = local.deploy_lambda ? 1 : 0
  depends_on = [terraform_data.build_image, aws_ecr_repository.ghrc_dmrpp_lambda]

  function_name = "${var.prefix}-ghrc-dmrpp"
  package_type = "Image"
  image_uri = "${aws_ecr_repository.ghrc_dmrpp_lambda[0].repository_url}:${local.image_version}"
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

resource "aws_ecr_repository" "ghrc_dmrpp_lambda" {
  count = local.deploy_lambda ? 1 : 0
  name                 = "${var.prefix}_ghrc_dmrpp_lambda"
  image_tag_mutability = "MUTABLE"
  force_delete = true

  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "terraform_data" "build_image" {
  count = local.deploy_lambda ? 1 : 0
  depends_on = [aws_ecr_repository.ghrc_dmrpp_lambda]
  triggers_replace = [var.docker_image]

  provisioner "local-exec" {
    command = <<-EOT
      docker pull ${var.docker_image}
      aws ecr get-login-password --region ${var.region} | docker login --username AWS --password-stdin ${var.account_id}.dkr.ecr.${var.region}.amazonaws.com
      docker tag ${var.docker_image} ${aws_ecr_repository.ghrc_dmrpp_lambda[0].repository_url}:${local.image_version}
      docker push ${aws_ecr_repository.ghrc_dmrpp_lambda[0].repository_url}:${local.image_version}
    EOT
  }
}
