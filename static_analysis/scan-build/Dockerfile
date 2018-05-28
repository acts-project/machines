FROM ubuntu:18.04

LABEL maintainer="Paul Gessinger <paul.gessinger@cern.ch>"


RUN apt-get update \
    && apt-get install -y clang clang-tools cmake iwyu \
    && apt-get install -y libeigen3-dev libboost-test-dev libboost-program-options-dev \
    && apt-get clean

ADD https://bootstrap.pypa.io/get-pip.py /root/get-pip.py
RUN cd /root && python get-pip.py

RUN pip --no-cache-dir install scan-build
