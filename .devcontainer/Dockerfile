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

# Set environment variables
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV SPARK_VERSION=3.5.5
ENV HADOOP_VERSION=3
ENV SPARK_HOME=/opt/spark
# Diese ENV PATH ist während des Build-Prozesses für RUN-Befehle nützlich
ENV PATH=$SPARK_HOME/bin:$JAVA_HOME/bin:$PATH

# Apache Spark herunterladen und installieren
RUN mkdir -p $SPARK_HOME && \
    curl -fsSL https://dlcdn.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz -o /tmp/spark.tgz && \
    tar -xzf /tmp/spark.tgz -C $SPARK_HOME --strip-components=1 && \
    rm -f /tmp/spark.tgz && \
    echo ">>>> Inhalt von $SPARK_HOME/bin während des Builds:" && \  # Hinzugefügt zur Fehlersuche (Debugging)
    ls -l $SPARK_HOME/bin  # Diese Zeile zeigt den Inhalt im Build-Log an

# Spark und Java zur PATH-Variable der Bash-Shell des Benutzers vscode hinzufügen
RUN echo '' >> /home/vscode/.bashrc && \
    echo '# Setze Umgebungsvariablen für Spark und Java' >> /home/vscode/.bashrc && \
    echo "export JAVA_HOME=${JAVA_HOME}" >> /home/vscode/.bashrc && \
    echo "export SPARK_HOME=${SPARK_HOME}" >> /home/vscode/.bashrc && \
    echo 'export PATH="$SPARK_HOME/bin:$JAVA_HOME/bin:$PATH"' >> /home/vscode/.bashrc  # Diese Zeile ist wichtig

WORKDIR /workspace