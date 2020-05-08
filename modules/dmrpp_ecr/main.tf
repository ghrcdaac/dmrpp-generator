//resource "aws_ecr_repository" "dmrpp_ecr" {
//  name                 = var.dmrpp_ecr_name
//  image_tag_mutability = "MUTABLE"
//  image_scanning_configuration {
//    scan_on_push = true
//  }
//}

//module "dmrpp_ecr" {
//  source = "https://github.com/ghrcdaac/terraform-aws-ecr-docker-image"
//  image_name  = "python-hello-world"
//  source_path = "${path.module}/src"
//}