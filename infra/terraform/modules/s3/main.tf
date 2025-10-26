resource "aws_s3_bucket" "post_images_bucket" {
  bucket = var.post_images_bucket_name
  tags = merge(var.tags)
}





