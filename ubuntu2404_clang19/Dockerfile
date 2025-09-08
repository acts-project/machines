FROM ubuntu:24.04

LABEL description="Ubuntu 24.04 with Acts dependencies"
LABEL maintainer="Stephen Nicholas Swatman <stephen.nicholas.swatman@cern.ch>"
# increase whenever any of the RUN commands change
LABEL version="2"
ARG CACHEBUST=0

# DEBIAN_FRONTEND ensures non-blocking operation (tzdata is a problem)
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update -y \
  && apt-get upgrade -y \
  && apt-get install -y wget

RUN wget -qO- https://apt.llvm.org/llvm-snapshot.gpg.key | tee /etc/apt/trusted.gpg.d/apt.llvm.org.asc
RUN echo "deb http://apt.llvm.org/noble/ llvm-toolchain-noble-19 main" >> /etc/apt/sources.list

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
    python3-venv \
    libsqlite3-dev \
    time \
    clang-19 \
    clang-tools-19 \
    gfortran \
    unzip \
    file \
  && apt-get clean -y

ENV CXX clang++-19
ENV CC clang-19

ENV ONNXRUNTIME_VERSION=1.21.0

RUN <<EOT bash
set -eux
set -o pipefail

_ARCH=\$(uname -m)

if [[ \$_ARCH == "x86_64" ]]; then
  url=https://github.com/microsoft/onnxruntime/releases/download/v${ONNXRUNTIME_VERSION}/onnxruntime-linux-x64-${ONNXRUNTIME_VERSION}.tgz
elif [[ \$_ARCH == "aarch64" || \$_ARCH == "arm64" ]]; then
  url=https://github.com/microsoft/onnxruntime/releases/download/v${ONNXRUNTIME_VERSION}/onnxruntime-linux-aarch64-${ONNXRUNTIME_VERSION}.tgz
fi
echo \$url

mkdir /onnxruntime_dl
curl --location --silent --create-dirs \$url \
  | tar -xz --strip-components=1 --directory /onnxruntime_dl


mkdir /onnxruntime_dl/onnxruntime
mv /onnxruntime_dl/include/* /onnxruntime_dl/onnxruntime
mv /onnxruntime_dl/onnxruntime /onnxruntime_dl/include

# Patch up `lib64 folder not existing in Ubuntu`
sed -i s/lib64/lib/g /onnxruntime_dl/lib/cmake/onnxruntime/onnxruntimeTargets-release.cmake

rsync -rl /onnxruntime_dl/ /usr/local/

EOT
