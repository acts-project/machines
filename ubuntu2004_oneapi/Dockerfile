FROM ubuntu:20.04

LABEL description="Ubuntu 20.04 with Acts dependencies"
LABEL maintainer="Paul Gessinger <paul.gessinger@cern.ch>"
# increase whenever any of the RUN commands change
LABEL version="1"

# DEBIAN_FRONTEND ensures non-blocking operation (tzdata is a problem)
ENV DEBIAN_FRONTEND noninteractive




RUN apt-get update -y \
  && apt-get install -y gnupg2 curl \
  && apt-get clean -y

RUN curl https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB | apt-key add - \
  && echo "deb https://apt.repos.intel.com/oneapi all main" > /etc/apt/sources.list.d/oneAPI.list

RUN apt-get update -y \
  && apt-get install -y \
    intel-oneapi-compiler-dpcpp-cpp-2021.2.0 \
  && apt-get clean -y

RUN apt-get update -y \
  && apt-get install -y \
    g++-8 \
    libstdc++-8-dev \
    cmake \
    git \
    libboost-dev \
    libboost-filesystem-dev \
    libboost-program-options-dev \
    libboost-test-dev \
    libeigen3-dev \
    ninja-build \
  # We don't want gcc9 to be present, because clang will pick it up
  && apt-get remove -y gcc-9 \
  && apt-get autoremove -y \
  && apt-get clean -y