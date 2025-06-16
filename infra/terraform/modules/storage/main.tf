resource "aws_s3_bucket" "raw" {
  bucket = "${var.env}-cv-raw"
  acl    = "private"
}
resource "aws_s3_bucket" "processed" {
  bucket = "${var.env}-cv-processed"
  acl    = "private"
}
resource "aws_s3_bucket" "models" {
  bucket = "${var.env}-cv-models"
  acl    = "private"
}