FROM jenkins/jenkins:jdk11

ENV JAVA_OPTS="-Djenkins.install.runSetupWizard=false"
### Adding admin user ### 

### Installing Plugins ####
COPY plugins.txt /usr/share/jenkins/ref/plugins.txt
RUN /usr/local/bin/install-plugins.sh < /usr/share/jenkins/ref/plugins.txt


COPY jenkins.yaml /usr/share/jenkins/ref/jenkins.yaml

### INSTALLING MAVEN Globally ###
USER root
RUN apt-get clean && apt-get update && apt-get install -y maven
USER jenkins

