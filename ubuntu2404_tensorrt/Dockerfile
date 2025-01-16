# Legal disclaimer:
# This software contains source code provided by NVIDIA Corporation

FROM nvcr.io/nvidia/tensorrt:24.12-py3
LABEL description="Ubuntu 24.04 with dependencies to build TensorRT inference component"
LABEL maintainer="Benjamin Huth <benjamin.huth@cern.ch"

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
  && apt-get clean -y

# manual builds for hep-specific packages
ENV GET curl --location --silent --create-dirs
ENV PREFIX /usr/local

# libtorch (unzip cannot be used in a pipe...)
ENV LIBTORCH_URL_GPU https://download.pytorch.org/libtorch/cu121/libtorch-cxx11-abi-shared-with-deps-2.3.1%2Bcu121.zip

RUN ${GET} https://github.com/Kitware/CMake/releases/download/v3.30.0/cmake-3.30.0-Linux-x86_64.tar.gz \
    | tar -xz --strip-components=1 --directory ${PREFIX}

RUN ${GET} https://acts.web.cern.ch/ACTS/ci/exatrkx/libtorch-cxx11-abi-shared-with-deps-2.3.1+cu121.tar.zst \
    | tar -I zstd -x --strip-components=1 --directory ${PREFIX}
