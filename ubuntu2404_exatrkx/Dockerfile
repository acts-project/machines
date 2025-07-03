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

RUN ${GET} https://download.pytorch.org/libtorch/cu128/libtorch-cxx11-abi-shared-with-deps-2.7.1%2Bcu128.zip \
  | bsdtar -xz --strip-components=1 --directory /usr/local

ENV ONNXRUNTIME_URL=https://github.com/microsoft/onnxruntime/releases/download/v1.21.0/onnxruntime-linux-x64-gpu-1.21.0.tgz


ENV ONNXRUNTIME_VERSION=1.21.0

RUN curl --location --silent --create-dirs $ONNXRUNTIME_URL \
  | tar -xz --strip-components=1 --directory /usr/local

ENV TORCH_SCATTER_VERSION=2.1.2

# torch-scatter
# I have absolutely no clue why I need this __CUDA_NO_HALF_CONVERSIONS__, but it fails to compile if not set...
RUN mkdir src \
  && ${GET} https://github.com/rusty1s/pytorch_scatter/archive/refs/tags/${TORCH_SCATTER_VERSION}.tar.gz \
    | ${UNPACK_TO_SRC} \
  && export TORCH_CUDA_ARCH_LIST="8.0 8.6 8.9 9.0" \
  && sed -i 's/CMAKE_CXX_STANDARD 14/CMAKE_CXX_STANDARD 17/' src/CMakeLists.txt \
  && head src/CMakeLists.txt \
  && cmake -B build -S src -GNinja \
    -DCMAKE_BUILD_TYPE=MinSizeRel \
    -DCMAKE_INSTALL_PREFIX=${PREFIX} \
    -DWITH_CUDA=ON \
    -DCMAKE_CUDA_FLAGS=-D__CUDA_NO_HALF_CONVERSIONS__ \
    -DCMAKE_CUDA_ARCHITECTURES=${CUDA_ARCH} \
  && cmake --build build -- install -j$(nproc) \
  && rm -rf build src
