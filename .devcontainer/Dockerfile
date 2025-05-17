FROM mcr.microsoft.com/devcontainers/python:3.10

# Install system dependencies
RUN apt-get update && apt-get install -y \
    unzip \
    curl \
    awscli \
    git \
    terraform \
    openjdk-11-jdk \
    && apt-get clean

# Set environment variables for Java and Spark
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV SPARK_VERSION=3.5.5
ENV HADOOP_VERSION=3
ENV SPARK_HOME=/opt/spark
ENV PATH=$PATH:$SPARK_HOME/bin

# Download and install Apache Spark
RUN mkdir -p $SPARK_HOME \
    && curl -L https://dlcdn.apache.org/spark/spark-3.5.5/spark-3.5.5-bin-hadoop3.tgz -o /tmp/spark.tgz \
    && tar -xvzf /tmp/spark.tgz -C $SPARK_HOME --strip-components=1 \
    && rm -f /tmp/spark.tgz

WORKDIR /workspace
