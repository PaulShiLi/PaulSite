# Bash version: 5.2.15
# FROM bash:5.2.15

# Node version: 19-slim
FROM node:19-slim

# Enable source command
SHELL ["/bin/bash", "-c"]

RUN apt-get update

# Install python
RUN apt-get install -y python3
RUN apt-get install -y python3-venv
RUN apt-get install -y python3-pip
RUN alias python=python3

# Install required packages
RUN apt-get install -y jq
RUN apt-get install -y net-tools

# Create directory to be used
RUN mkdir -p /var/www/PaulWebsite

# Copy files to working directory
COPY . /var/www/PaulWebsite

# Set working directory
WORKDIR /var/www/PaulWebsite

ENV LISTEN_PORT=8080
EXPOSE 8080

# Install Dependencies from build.sh
RUN source ./build.sh -d

RUN pip install -r requirements.txt

CMD [ "bash", "./run.sh" ]