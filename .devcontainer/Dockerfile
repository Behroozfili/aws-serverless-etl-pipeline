FROM mcr.microsoft.com/devcontainers/python:3.10

# Install only essential system dependencies not handled by features.
# Java, Terraform, AWS CLI, and Git will be installed via devcontainer features.
RUN apt-get update && apt-get install -y \
    unzip \
    curl \
    # سایر وابستگی‌های سیستمی که توسط features پوشش داده نمی‌شوند
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for Spark installation (JAVA_HOME is set by feature)
ENV SPARK_VERSION=3.5.5
ENV HADOOP_VERSION=3
ENV SPARK_HOME=/opt/spark
# PATH را اینجا برای دستورات RUN تنظیم می‌کنیم،
# اما PATH نهایی کاربر از .bashrc (که توسط postCreateCommand ویرایش می‌شود) خواهد آمد.
# JAVA_HOME در زمان build ممکن است هنوز توسط feature تنظیم نشده باشد،
# پس برای نصب Spark به آن ارجاع نمی‌دهیم، مگر اینکه بدانیم feature قبل از این RUN اجرا شده.
# فرض می‌کنیم نصب Spark به JAVA_HOME در زمان اجرا نیاز دارد که توسط postCreateCommand تنظیم می‌شود.
ENV PATH=$SPARK_HOME/bin:$PATH


# Download and install Apache Spark
# این بخش به JAVA_HOME در زمان build نیازی ندارد، فقط در زمان اجرا لازم است.
RUN mkdir -p $SPARK_HOME && \
    curl -fsSL https://dlcdn.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz -o /tmp/spark.tgz && \
    tar -xzf /tmp/spark.tgz -C $SPARK_HOME --strip-components=1 && \
    rm -f /tmp/spark.tgz && \
    echo ">>>> Contents of $SPARK_HOME/bin after Spark installation:" && \
    ls -l $SPARK_HOME/bin

WORKDIR /workspace
COPY ../ml-model/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt