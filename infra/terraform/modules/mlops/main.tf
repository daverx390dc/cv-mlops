data "aws_iam_policy_document" "sm_assume" {
  statement {
    effect = "Allow"
    principals { type = "Service" identifiers = ["sagemaker.amazonaws.com"] }
    actions = ["sts:AssumeRole"]
  }
}
resource "aws_iam_role" "sagemaker_execution" {
  name               = "${var.env}-sm-exec"
  assume_role_policy = data.aws_iam_policy_document.sm_assume.json
}
resource "aws_iam_role_policy_attachment" "sm_policy" {
  role       = aws_iam_role.sagemaker_execution.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSageMakerFullAccess"
}