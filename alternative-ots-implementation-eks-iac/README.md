# Intro and Context (THIS IS WIP and FOR REFRENCE ONLY) 
This implementation is a work in progress based on the configurable templates. This is fully automated IaC and DevOps toolchain setup but not completely compliant with requirements but pretty much same. This must be run on AWS (tightly coupled). This should only be consider as another approach to solve the same problem quickly based on configurable ready made templates.

# Tools and utilities:
- Jenkins  
- SonarQube
- Docker 
- AWS EKS Managed Kubernetes Cluster
- Kubectl
- Terraform


Folder Structure Conventions
============================

> Folder structure options and naming conventions for this projects

### A typical top-level directory layout

    .
    ├── demoapp        		# Helm chart
    ├── eks  				# Infrastructure provising
    ├── terraform 			# IAM and S3 setup
	├── pipeline-registry 	# YAMLS of the project Jenkins, Sonar
    └── README.md

> Use short lowercase names at least for the top-level files and folders except
> `LICENSE`, `README.md`

Steps to follow - WIP
=====================

1) unzip the file first
2) you will find a file named as 'eks'
3) In EKS folder there is another file named as 'modules'
4) execute main.tf
5) it will create autoscaling groups, master nodes, slave nodes, workers and vpc peering
6) you can verify the cluster from AWS console
7) In order to test, you can kill a node and it will be provisioned automatically again
8) Than you will find another folder named as 'terraform'
9) In this folder you will find 2 terraforms.... One is for IAM and other one is for S3
10) execute both the terraforms and it will create necessary IAM roles and permissions. S3 bucket is necessary for cluster.
11) Than you will find another folder named as 'pipeline-registry'
12) In this you will find Jenkins yamls. Execute them it will setup Sonar automatically.
13) Since the project repo is already setup, We need to link and execute a job.