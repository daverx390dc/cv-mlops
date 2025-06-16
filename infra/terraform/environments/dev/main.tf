provider "aws" {
  region = var.aws_region
}
module "networking" {
  source     = "../../modules/networking"
  env        = "dev"
  cidr_block = "10.0.0.0/16"
}
# similar calls for storage, compute, mlops