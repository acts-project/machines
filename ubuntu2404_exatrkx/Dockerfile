FROM nvidia/cuda:12.8.1-cudnn-devel-ubuntu24.04
LABEL description="Ubuntu 24.04 with Acts dependencies for the Exa.TrkX Plugin"
LABEL maintainer="Paul Gessinger <paul.gessinger@cern.ch"
# increase whenever any of the RUN commands change
LABEL version="1"

# DEBIAN_FRONTEND ensures non-blocking operation (tzdata is a problem)
ENV DEBIAN_FRONTEND noninteractive

# install dependencies from the package manager.
#
# see also https://root.cern.ch/build-prerequisites
RUN apt-get update -y \
  && apt-get upgrade -y \
  && apt-get install -y \
    build-essential \
    curl \
    git \
    freeglut3-dev \
    libexpat-dev \
    libftgl-dev \
    libgl2ps-dev \
    libglew-dev \
    libgsl-dev \
    liblz4-dev \
    liblzma-dev \
    libpcre3-dev \
    libx11-dev \
    libxext-dev \
    libxft-dev \
    libxpm-dev \
    libxerces-c-dev \
    libzstd-dev \
    zstd \
    ninja-build \
    python3 \
    python3-dev \
    python3-pip \
    rsync \
    unzip \
    zlib1g-dev \
    ccache \
    libsqlite3-dev \
    time \
    libarchive-tools \
    cmake \
  && apt-get clean -y

# manual builds for hep-specific packages
ENV GET curl --location --silent --create-dirs
ENV UNPACK_TO_SRC tar -xz --strip-components=1 --directory src
ENV PREFIX /usr/local
ENV CUDA_ARCH 86

RUN ${GET} -o libtorch.zip https://download.pytorch.org/libtorch/cu128/libtorch-cxx11-abi-shared-with-deps-2.7.1%2Bcu128.zip \
  | bsdtar -xz --strip-components=1 --directory /usr/local

ENV ONNXRUNTIME_URL=https://github.com/microsoft/onnxruntime/releases/download/v1.21.0/onnxruntime-linux-x64-gpu-1.21.0.tgz


ENV ONNXRUNTIME_VERSION=1.21.0

RUN curl --location --silent --create-dirs $ONNXRUNTIME_URL \
  | tar -xz --strip-components=1 --directory /usr/local

