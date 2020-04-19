#Profile Name
profile = "prod"

#Policies ARN
centralized-logging-policy-arn = "arn:aws:iam::${data.aws_caller_identity.account_id}:policy/centralized-logging-policy"
autoscaling-elb-policy-arn = "arn:aws:iam::${data.aws_caller_identity.account_id}:policy/prod-autoscaling-elb-policy"
secret-manager-application-policy-arn = "arn:aws:iam::${data.aws_caller_identity.account_id}:policy/prod-secret-application-policy"
