terraform {
  backend "s3" {
    bucket = "iac"
    key    = "s3/s3.tfstate"
    region = "eu-west-1"
    workspace_key_prefix = "statefiles"
    profile = "default"
  }
}
