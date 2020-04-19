data "template_file" "policy_document" {
  template = "${file(format("%s/%s-policy.json", var.profile, var.service_name))}"
}

#your Service Policies
module "your-service-policy" {
  source       = "<terraform-refrence>"
  name         = "${format("%s-%s-policy", var.profile, var.service_name)}"
  path         = "/"
  description  = "${format("IAM policy for %s", var.service_name)}"
  policy       = "${data.template_file.policy_document.rendered}"
}

#Instance Profile
module "your-service-instance-profile" {
  source       = "<terraform-refrence>"
  service_name = "${var.service_name}"
  cteam        = "${var.c_team}"
  cservice     = "${var.c_service}"
  cenv         = "${var.profile}"
}

#your-Service Policy Attachment
resource "aws_iam_role_policy_attachment" "your_service_policy_attachment" {
  role       = "${module.your-service-instance-profile.role_name}"
  policy_arn = "${module.your-service-policy.arn}"
}

#Centralized-Logging Policy Attachment
resource "aws_iam_role_policy_attachment" "centralized_logging_policy_attachment" {
  role       = "${module.your-service-instance-profile.role_name}"
  policy_arn = "${var.centralized-logging-policy-arn}"
}

#Autoscaling-ELB Policy Attachment
resource "aws_iam_role_policy_attachment" "autoscaling_elb_policy_attachment" {
  role       = "${module.your-service-instance-profile.role_name}"
  policy_arn = "${var.autoscaling-elb-policy-arn}"
}

#Secret-Manager-Application Policy Attachment
resource "aws_iam_role_policy_attachment" "secret_manager_application_policy_attachment" {
  role       = "${module.your-service-instance-profile.role_name}"
  policy_arn = "${var.secret-manager-application-policy-arn}"
}
