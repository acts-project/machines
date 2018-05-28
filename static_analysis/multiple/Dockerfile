FROM ubuntu:18.04
LABEL maintainer="Paul Gessinger <paul.gessinger@cern.ch>"

RUN apt-get update \
    && apt-get install -y \
       curl \
       python3 \
       python3-pip \
       python-yaml \
       python3-lxml \
       build-essential \
       cmake \
       libeigen3-dev \
       libboost-program-options-dev \
       libboost-test-dev \
       clang-6.0 \
       clang-tidy-6.0 \
       clang-tools-6.0 \
       cppcheck \
    && rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/bin/pip3 /usr/bin/pip

RUN curl -L -o oclint.tar.gz https://github.com/oclint/oclint/releases/download/v0.13.1/oclint-0.13.1-x86_64-linux-4.4.0-112-generic.tar.gz \
    && tar xzvf oclint.tar.gz -C /opt \
    && mv /opt/oclint* /opt/oclint \
    && rm oclint.tar.gz

RUN ln -sf /usr/bin/clang-tidy-6.0 /usr/bin/clang-tidy \
    && ln -sf /usr/bin/run-clang-tidy-6.0.py /usr/bin/run-clang-tidy.py

RUN pip --no-cache-dir install codereport scan-build

ENV PATH /opt/oclint/bin:$PATH

WORKDIR /src
