resource "aws_ecr_repository" "ml_images" {
  name = "${var.env}-cv-images"
  image_scanning_configuration { scan_on_push = true }
}
resource "aws_ecs_cluster" "this" {
  name = "${var.env}-ecs"
}