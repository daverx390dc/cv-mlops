provider "aws" {
  region = var.aws_region
}
module "networking" {
  source     = "../../modules/networking"
  env        = "prod"
  cidr_block = "10.1.0.0/16"
}
# similar calls for storage, compute, mlops