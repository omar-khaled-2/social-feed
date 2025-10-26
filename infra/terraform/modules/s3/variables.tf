variable "post_images_bucket_name" {
    type    = string
    default = "post_images"
}
variable "tags" {
  type    = map(string)
  default = {}
}
