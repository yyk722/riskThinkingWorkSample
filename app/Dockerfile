# BUILD: docker build --rm -t 
FROM python:3.10
LABEL maintainer="Ken"

# Never prompts the user for choices on installation/configuration of packages
ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux
ENV PYTHON_TA_LIB_VERSION "0.4.24"

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git && \
    apt-get install -y gcc && \
    apt-get install -y g++


# Define en_US.
ENV LANGUAGE en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV LC_CTYPE en_US.UTF-8
ENV LC_MESSAGES en_US.UTF-8

COPY . /

RUN pip install -r requirements.txt

ENV PATH=$PATH:/opt/java/jdk-15.0.2/bin

RUN mkdir /opt/java && \
    curl https://download.java.net/java/GA/jdk15.0.2/0d1cfde4252546c6931946de8db48ee2/7/GPL/openjdk-15.0.2_linux-x64_bin.tar.gz | tar -xz -C /opt/java/

# TA-Lib
RUN cd /tmp \
    && curl -L -O http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz \
    && tar -zxf ta-lib-0.4.0-src.tar.gz \
    && cd ta-lib/ \
    && ./configure --prefix=/usr \
    && make \
    && make install \
    && pip3 install setuptools numpy \
    && pip3 install ta-lib==${PYTHON_TA_LIB_VERSION} \
    && rm -rf /root/.cache \
              /tmp/* \
              /var/cache/apk/* \
              /var/lib/apk/lists/*

WORKDIR /