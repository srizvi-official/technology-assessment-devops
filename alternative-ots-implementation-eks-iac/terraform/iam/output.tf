output "arn" {
  description = "The ARN assigned by AWS to this policy"
  value       = "${module.your-service-policy.arn}"
}
