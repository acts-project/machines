FROM ubuntu:22.04

LABEL description="Ubuntu 22.04 with Acts dependencies"
LABEL maintainer="Paul Gessinger <paul.gessinger@cern.ch>"
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
    git-lfs \
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
    libxxhash-dev \
    libzstd-dev \
    zstd \
    ninja-build \
    python3 \
    python3-dev \
    python3-pip \
    rsync \
    zlib1g-dev \
    ccache \
    libsqlite3-dev \
    time \
  && apt-get clean -y

# manual builds for hep-specific packages
ENV GET curl --location --silent --create-dirs
ENV UNPACK_TO_SRC tar -xz --strip-components=1 --directory src
ENV PREFIX /usr/local

ENV ONNXRUNTIME_VERSION=1.18.1

RUN ${GET} https://github.com/Kitware/CMake/releases/download/v3.30.0/cmake-3.30.0-Linux-x86_64.tar.gz \
    | tar -xz --strip-components=1 --directory ${PREFIX}

# Onnx (download of tar.gz does not work out of the box, since the build.sh script requires a git repository)
RUN git clone https://github.com/microsoft/onnxruntime src \
  && (cd src && git checkout v${ONNXRUNTIME_VERSION}) \
  && ./src/build.sh \
    --config MinSizeRel \
    --build_shared_lib \
    --build_dir build \
    --parallel $(nproc) \
    --skip_tests \
    --parallel 0 \
    --allow_running_as_root \
  && cmake --build build/MinSizeRel -- install \
  && rm -rf build src
