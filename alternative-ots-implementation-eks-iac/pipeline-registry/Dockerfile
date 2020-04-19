FROM python:3

RUN mkdir registry
WORKDIR registry
COPY . /registry
RUN apt-get update -y && apt-get install -y unzip
RUN pip install -r ops/bin/requirements.txt

# Installing sonar-scanner
RUN wget https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-3.2.0.1227-linux.zip && \
    unzip sonar-scanner-cli-3.2.0.1227-linux.zip && \
    mv sonar-scanner-3.2.0.1227-linux /opt/ && \
    cd /usr/local/bin && \
    ln -s /opt/sonar-scanner-3.2.0.1227-linux/bin/sonar-scanner sonar-scanner && \
    cd - && \
    rm -rf sonar-scanner-cli-3.2.0.1227-linux.zip

