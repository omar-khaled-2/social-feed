variable "region" {
  default = "us-east-1"
}

variable "tags" {
  type = map(string)
  default = {
    Project = "myproject"
    Env     = "dev"
  }
}
