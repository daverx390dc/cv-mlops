resource "aws_vpc" "this" {
  cidr_block = var.cidr_block
  tags       = { Name = "${var.env}-vpc" }
}
resource "aws_subnet" "public" {
  count                   = 2
  vpc_id                  = aws_vpc.this.id
  cidr_block              = cidrsubnet(var.cidr_block, 8, count.index)
  map_public_ip_on_launch = true
  tags                    = { Name = "${var.env}-public-${count.index}" }
}