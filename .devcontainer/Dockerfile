FROM mcr.microsoft.com/devcontainers/python:3.10


RUN apt-get update && apt-get install -y \
    unzip \
    curl \
    awscli \
    git \
    terraform \
    && apt-get clean


WORKDIR /workspace
