# Objective
In this exercise we need to create automated Kubernetes deployment, this deployment must build Jenkins &amp; Sonar docker images and &amp; run on Kubernetes. Jenkins Docker must have maven support, Java 11 support. Jenkins pipeline must work smoothly once the setup is complete.


# Tools and utilities:
Jenkins
 - Apache Maven 3.3
 - Java 11
SonarQube
Docker 
AWS EKS (Managed Kubernetes Cluster)
Kubectl


Folder Structure Conventions
============================

> Folder structure options and naming conventions for this projects

### A typical top-level directory layout

    .
    ├── docker_resources        # Contains Dockerfile for resources
    ├── deployment_descriptors  # Kubernetes Orchestration Definitions
    └── README.md

> Use short lowercase names at least for the top-level files and folders except
> `LICENSE`, `README.md`



