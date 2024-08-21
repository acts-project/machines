FROM nvidia/cuda:12.1.0-cudnn8-devel-ubuntu22.04
LABEL description="Ubuntu 20.04 with Acts dependencies for the Exa.TrkX Plugin"
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
  && apt-get clean -y

# manual builds for hep-specific packages
ENV GET curl --location --silent --create-dirs
ENV UNPACK_TO_SRC tar -xz --strip-components=1 --directory src
ENV PREFIX /usr/local
ENV CUDA_ARCH 86

ENV XXHASH_VERSION=0.7.3
ENV JSON_VERSION=3.11.2
ENV ROOT_VERSION=6.28.06
ENV TORCH_SCATTER_VERSION=2.1.2
ENV ONNXRUNTIME_VERSION=1.18.1

# libtorch (unzip cannot be used in a pipe...)
ENV LIBTORCH_URL_GPU https://download.pytorch.org/libtorch/cu121/libtorch-cxx11-abi-shared-with-deps-2.3.1%2Bcu121.zip

RUN ${GET} https://github.com/Kitware/CMake/releases/download/v3.30.0/cmake-3.30.0-Linux-x86_64.tar.gz \
    | tar -xz --strip-components=1 --directory ${PREFIX}

# xxHash
RUN mkdir -p src \
  && ${GET} https://github.com/Cyan4973/xxHash/archive/v${XXHASH_VERSION}.tar.gz \
    | ${UNPACK_TO_SRC} \
  && cmake -B build -S src/cmake_unofficial -GNinja\
    -DCMAKE_BUILD_TYPE=MinSizeRel \
    -DCMAKE_CXX_STANDARD=20 \
    -DCMAKE_INSTALL_PREFIX=${PREFIX} \
  && cmake --build build -- install -j$(nproc) \
  && rm -rf build src


RUN ${GET} https://acts.web.cern.ch/ACTS/ci/exatrkx/libtorch-cxx11-abi-shared-with-deps-2.3.1+cu121.tar.zst \
    | tar -I zstd -x --strip-components=1 --directory ${PREFIX}

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

# Onnx (download of tar.gz does not work out of the box, since the build.sh script requires a git repository)
RUN git clone https://github.com/microsoft/onnxruntime src \
  && (cd src && git checkout v${ONNXRUNTIME_VERSION}) \
  && ./src/build.sh \
    --config MinSizeRel \
    --build_shared_lib \
    --build_dir build \
    --use_cuda \
    --cuda_home /usr/local/cuda \
    --cudnn_home /usr/local/cuda \
    --skip_tests \
    --parallel 0 \
    --allow_running_as_root \
    --cmake_extra_defines \
      CMAKE_INSTALL_PREFIX=${PREFIX} \
      CMAKE_CUDA_ARCHITECTURES=${CUDA_ARCH} \
  && cmake --build build/MinSizeRel -- install \
  && rm -rf build src
