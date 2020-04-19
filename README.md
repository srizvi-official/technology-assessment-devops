# Objective
In this exercise we need to create automated Kubernetes deployment, this deployment must build Jenkins &amp; Sonar docker images and &amp; run on Kubernetes. Jenkins Docker must have maven support, Java 11 support. Jenkins pipeline must work smoothly once the setup is complete.

# Tools and utilities:
- Docker  
- Kubectl
- Helm
- kustomize
- Curl

Prerequisite
============

- Running Kubernetes Cluster (We can provision it using any IaC tool standard definitions)
- Kubectl utility configured
- Linux OS
- These ports must whitelisted 8080 and 9000 
- Cloud Environment (AWS EKS, GCE GKE, AZURE AKS)

Folder Structure Conventions
============================

> Folder structure options and naming conventions for this projects

### A typical top-level directory layout

	.
    ├── alternative-ots-implementation-eks-iac  # Off the shelf implementation using standard configurable scripts - WIP (follow respective readme) 
    ├── tailored-implementation  				# Tailored implementation as per given ask (kept it very simple) - (scope of this task)
    └── README.md								# For current implementation follow this Readme and `tailored-implementation` folder. 

> Use short lowercase names at least for the top-level files and folders except
> `LICENSE`, `README.md`

Decision Making Process
=======================

Thought process behind giving two implementations is to demonstrate options and their tradeoffs. Option A (off the shelf) is fast and comprehensive but less flexible. While, option B (bespoke) takes time but more precise and flexible. If we nderstand the trade offs better then both approaches are very handy. choices always helps.


**Approach A**: is ready made scripts with little modifications to setup things fast. Rational is just to put another option on table.
**Approach B**: is simple and flexible but limited. Due to time constraint I didn't implement the helm chart in this solution, but, if I get time will do over the weekend. 

- I created custom image of Jenkins because configiration automation is required.
- I used SonarQube image from registery hub directly as no customization is required.


Tailored Implementation
=======================

Browse directory structure of main project.

### A typical sub-level directory layout
```
.
	├── docker-source					# holds code for pre-configured Jenkins server 
	│   ├── Dockerfile						# Jenkins DockerFile - this definition used to create image for Kubernetes container
	│   ├── jenkins.yaml					# Jenkins Configuration as a code (pre-configured job with polling every 5 mins, Repo URL)
	│   └── plugins.txt						# Plugins list to install by default
	├── k8s-orchestration				# holds manifests for Kubernetes cluster orchestration (`srtategy: one file per resource group`)
	│   ├── namespace.yml					# project namespace which create virtual isolated layer in cluster (help in troubleshooot)
	│   ├── sonarqube.yml					# deployment file Sonar resource group includes services, pods, secrets, configmap, deployment, mysql (external) etc.
	│   ├── jenkins.yml						# deployment file Jenkins resource group includes services, pods, persistant volume, configmap, deployment.
	│   └── ingress_nginx_compiled.yml		# Alternative, Ingress controller implementation not in active use. Load balancer are used.
	├── docs											# Bonus task: Kubernetes component diagram for this project. (helm chart -> facing time constraint)
	│   ├── k8s-alternative-components-orchestration-flow.png	# This is now we can configure using ingress file (Ingress controller)	
	│   └── k8s-active-components-orchestration-flow.png		# This how current solution is implemented (load balancer)	
	│   └── helm-charts-delivery-pipeline						# Helm chart for this project - WIP (need to configure it)		
    └── README.md	
```    
> Use short lowercase names at least for the top-level files and folders except
> `LICENSE`, `README.md`

Kubernetes Components / Orchbestration - Approach Load balancer (Bonus Activity) 
================================================================================
**Note:** This approach is use for the feasability but not good for production grade deployments with multiple microservices. But, good for building, testing and exposing test projects.

![k8s-active-components-orchestration-flow](https://raw.githubusercontent.com/srizvi-official/technology-assessment-devops/master/tailored-implementation/docs/k8s-active-components-orchestration-flow.png)

Kubernetes Components / Orchbestration - Approach Ingress Controller (Bonus Activity)
=====================================================================================

**Note:** I have implemented this approach but didn't used it because dns and domain is private (which is configured). But, its is good for production grade deployments.

![k8s-alternative-components-orchestration-flow](https://raw.githubusercontent.com/srizvi-official/technology-assessment-devops/master/tailored-implementation/docs/k8s-alternative-components-orchestration-flow.png)


Steps to Follow
===============
```
1) Clone code to your work space.
2) Make sure prerequisite are ready.
3) Docker images are already created but source files are in `tailored-implementation/docker-source` folder. (skip this step unless you want to create new image)

#Create images with given DockerFile(s)
docker build -t testappstudio/delivery-pipeline:jenkins

#Push images to image registery service (contact me at srizvi@csquareonline.com for credentials)
docker login
docker push testappstudio/delivery-pipeline:jenkins

4) Execute following commands in given sequence (you can spin SonarQube and Jenkins independenly as well, if want to)

#to create namespace
kubectl apply -f namespace.yml

#to create sonarqube
kubectl apply -f sonarqube.yml

#to create jenkins
kubectl apply -f jenkins.yml

#optional for ingress nginx setup (skip this for default implementation: which is using loadbalancer)
kubectl apply -f ingress_nginx_compiled.yml

#to access cluster Pods, Service  (see expose IPs to access Jenkins & sonarQube from browser)
kubectl get all,pv -n delivery-pipeline

#Sonar credentials
username : admin
Password : admin

Jenkins credentials:
username: admin
Password: admin123

5) First job will auto trigger in 5 mins then start polling (Poll SCM: https://bitbucket.org/gabriel-a/template-microservice.git)
6) SonarQube configuration

Create a webhook programmatically by hitting SonarQube API (Replace the placeholder in below command before execution) 
curl "http://admin:admin@<SONAR_EXTERNAL_IP>:<SONAR_PORT>/api/webhooks/create" -X POST -d "name=jenkins&url=http://jenkins-service:8080/sonarqube-webhook/"

After Interpolation its look like (example)
"http://admin:admin@35.232.117.174:9000/api/webhooks/create" -X POST -d "name=jenkins&url=http://jenkins-service:8080/sonarqube-webhook/"

On success you will receive following
{"webhook":{"key":"AXGP3k5nfDBDMMWYZ_WB","name":"jenkins","url":"http://jenkins-service:8080/sonarqube-webhook/"}
 
7) Login to Jenkins and see the results of the delivery pipeline.

8) I have executed it myself (end to end) and all the stages passed successfully :)

**Note:** We can put all the commands in batch script if we want to execute this like a single job and completely automate it. 
```
