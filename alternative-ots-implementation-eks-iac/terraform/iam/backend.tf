terraform {
  backend "s3" {
    bucket = "iacv2-qa"
    key    = "iam/iam.tfstate"
    region = "eu-west-1"
    workspace_key_prefix = "statefiles"
    profile = "default"
  }
}
