resource "aws_s3_bucket" "bucket" {
  bucket = "${var.bucketname}"
  acl    = "${var.acl}"

  tags = {
    c-team		= ""
    c-service	= ""
    c-domain	= ""
    c-subdomain = ""
    c-criticality = "high" 
  }
}