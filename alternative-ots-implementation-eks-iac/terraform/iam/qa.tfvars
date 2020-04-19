#Profile Name
profile = "qa"

#Policies ARN
centralized-logging-policy-arn = "arn:aws:iam::${data.aws_caller_identity.account_id}:policy/centralized-logging-policy"
autoscaling-elb-policy-arn = "arn:aws:iam::${data.aws_caller_identity.account_id}:policy/qa-autoscaling-elb-policy"
secret-manager-application-policy-arn = "arn:aws:iam::${data.aws_caller_identity.account_id}:policy/qa-secret-application-policy"
