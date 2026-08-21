FROM ubuntu:26.04

LABEL description="Ubuntu 26.04 with Acts dependencies"
LABEL maintainer="Paul Gessinger <paul.gessinger@cern.ch>"
# increase whenever any of the RUN commands change
LABEL version="1"
ARG CACHEBUST=0

# DEBIAN_FRONTEND ensures non-blocking operation (tzdata is a problem)
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y \
  && apt-get upgrade -y \
  && apt-get install -y wget ca-certificates

RUN wget -qO /etc/apt/keyrings/apt.llvm.org.asc https://apt.llvm.org/llvm-snapshot.gpg.key
RUN printf '%s\n' \
    'Types: deb' \
    'URIs: http://apt.llvm.org/resolute/' \
    'Suites: llvm-toolchain-resolute-22' \
    'Components: main' \
    'Signed-By: /etc/apt/keyrings/apt.llvm.org.asc' \
    > /etc/apt/sources.list.d/llvm.sources

# install dependencies from the package manager.
#
# see also https://root.cern.ch/build-prerequisites
RUN apt-get update -y \
  && apt-get upgrade -y \
  && apt-get install -y \
    build-essential \
    curl \
    git \
    git-lfs \
    cmake \
    freeglut3-dev \
    libexpat-dev \
    libftgl-dev \
    libgl1-mesa-dev \
    libgl2ps-dev \
    libglew-dev \
    libgsl-dev \
    liblz4-dev \
    liblzma-dev \
    libpcre2-dev \
    libx11-dev \
    libxext-dev \
    libxft-dev \
    libxpm-dev \
    libxerces-c-dev \
    libxxhash-dev \
    libzstd-dev \
    libcrypt-dev \
    zstd \
    ninja-build \
    python3 \
    python3-dev \
    python3-pip \
    rsync \
    zlib1g-dev \
    ccache \
    python3-venv \
    libsqlite3-dev \
    time \
    clang-22 \
    clang-tools-22 \
    gfortran \
    unzip \
    file \
    bc \
  && apt-get clean -y

ENV CXX=clang++-22
ENV CC=clang-22
