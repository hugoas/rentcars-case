FROM apache/airflow:2.7.1

USER root

RUN apt-get update && \
    apt-get install -y openjdk-11-jdk procps && \
    apt-get clean

ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

USER airflow