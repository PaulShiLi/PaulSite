# Bash version: 5.2.15
# FROM bash:5.2.15

# Node version: 19-slim
FROM nikolaik/python-nodejs:python3.11-nodejs20-slim

# Enable source command
SHELL ["/bin/bash", "-c"]

RUN apt-get update

# Install python
RUN alias python=python3

# Install required packages
RUN apt-get install -y jq
RUN apt-get install -y net-tools

RUN npm install -g npm@latest

VOLUME ["/var/www/psliSite"]

# Set working directory
WORKDIR /var/www/psliSite

RUN pip install gunicorn uvicorn

COPY requirements.txt .
RUN pip install -r requirements.txt

# WORKDIR /var/www/psliSite/assets/node
# RUN npm install tailwindcss
# WORKDIR /var/www/psliSite

COPY env.json .

COPY ./pkgs/cmd/exportEnv.sh ./pkgs/cmd/exportEnv.sh
RUN bash ./pkgs/cmd/exportEnv.sh

ENV LISTEN_PORT=8080
EXPOSE 8080

ENTRYPOINT ["bash", "/var/www/psliSite/pkgs/cmd/run.sh", "-d"]
