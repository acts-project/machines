FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu20.04

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
  && apt-get install -y \
    build-essential \
    curl \
    git \
    freeglut3-dev \
    libboost-dev \
    libboost-filesystem-dev \
    libboost-program-options-dev \
    libboost-test-dev \
    libexpat-dev \
    libeigen3-dev \
    libftgl-dev \
    libgl2ps-dev \
    libglew-dev \
    libgsl-dev \
    liblz4-dev \
    liblzma-dev \
    libpcre3-dev \
    libtbb-dev \
    libx11-dev \
    libxext-dev \
    libxft-dev \
    libxpm-dev \
    libxerces-c-dev \
    libzstd-dev \
    ninja-build \
    python3 \
    python3-dev \
    python3-pip \
    rsync \
    unzip \
    zlib1g-dev \
    ccache \
  && apt-get clean -y

# manual builds for hep-specific packages
ENV GET curl --location --silent --create-dirs
ENV UNPACK_TO_SRC tar -xz --strip-components=1 --directory src
ENV PREFIX /usr/local
ENV CUDA_ARCH 86

# CMake 3.16.3 version in APT is too old
# requires rsync; installation uses `rsync` instead of `install`
RUN mkdir src \
  && ${GET} https://github.com/Kitware/CMake/releases/download/v3.21.2/cmake-3.21.2-Linux-x86_64.tar.gz \
    | ${UNPACK_TO_SRC} \
  && rsync -ruv src/ ${PREFIX} \
  && cd .. \
  && rm -rf src

# xxHash
RUN mkdir -p src \
  && ${GET} https://github.com/Cyan4973/xxHash/archive/v0.7.3.tar.gz \
    | ${UNPACK_TO_SRC} \
  && cmake -B build -S src/cmake_unofficial -GNinja\
    -DCMAKE_BUILD_TYPE=MinSizeRel \
    -DCMAKE_INSTALL_PREFIX=${PREFIX} \
  && cmake --build build -- install \
  && rm -rf build src

# nlohmann's JSON
RUN mkdir src \
  && ${GET} https://github.com/nlohmann/json/archive/refs/tags/v3.10.2.tar.gz \
    | ${UNPACK_TO_SRC} \
  && cmake -B build -S src -GNinja \
    -DCMAKE_BUILD_TYPE=MinSizeRel \
    -DJSON_BuildTests=OFF \
  && cmake --build build -- install \
  && rm -rf build src

# libtorch (unzip cannot be used in a pipe...)
ENV LIBTORCH_URL_GPU https://download.pytorch.org/libtorch/cu118/libtorch-cxx11-abi-shared-with-deps-2.0.1%2Bcu118.zip
ENV LIBTORCH_URL_CPU https://download.pytorch.org/libtorch/cpu/libtorch-cxx11-abi-shared-with-deps-2.0.1%2Bcpu.zip

RUN ${GET} --output libtorch.zip ${LIBTORCH_URL_GPU} \
  && unzip libtorch.zip \
  && rsync -ruv libtorch/ ${PREFIX} \
  && rm -rf libtorch*

# torch-scatter
# I have absolutely no clue why I need this __CUDA_NO_HALF_CONVERSIONS__, but it fails to compile if not set...
RUN mkdir src \
  && ${GET} https://github.com/rusty1s/pytorch_scatter/archive/refs/tags/2.0.9.tar.gz \
    | ${UNPACK_TO_SRC} \
  && cmake -B build -S src -GNinja \
    -DCMAKE_BUILD_TYPE=MinSizeRel \
    -DCMAKE_CXX_STANDARD=17 \
    -DCMAKE_INSTALL_PREFIX=${PREFIX} \
    -DWITH_CUDA=ON \
    -DCMAKE_CUDA_FLAGS=-D__CUDA_NO_HALF_CONVERSIONS__ \
    -DCMAKE_CUDA_ARCHITECTURES=${CUDA_ARCH} \
  && cmake --build build -- install \
  && rm -rf build src

# ROOT
RUN mkdir src \
  && ${GET} https://root.cern/download/root_v6.24.06.source.tar.gz \
    | ${UNPACK_TO_SRC} \
  && cmake -B build -S src -GNinja \
    -DCMAKE_BUILD_TYPE=MinSizeRel \
    -DCMAKE_CXX_STANDARD=17 \
    -DCMAKE_INSTALL_PREFIX=${PREFIX} \
    -Dfail-on-missing=ON \
    -Dgminimal=ON \
    -Dgdml=ON \
    -Dopengl=ON \
    -Dpyroot=ON \
  && cmake --build build -- install \
  && rm -rf build src

# cugraph
RUN mkdir src \
  && ${GET} https://github.com/rapidsai/cugraph/archive/refs/tags/v22.02.00.tar.gz \
    | ${UNPACK_TO_SRC} \
  && cmake -B build -S src/cpp -GNinja \
    -DCMAKE_BUILD_TYPE=MinSizeRel \
    -DCMAKE_CXX_STANDARD=17 \
    -DCMAKE_INSTALL_PREFIX=${PREFIX} \
    -DCMAKE_CUDA_ARCHITECTURES=${CUDA_ARCH} \
    -DBUILD_TESTS=OFF \
    -DBUILD_CUGRAPH_MG_TESTS=OFF \
  && cmake --build build -- install \
  && rm -rf build src

# Onnx (download of tar.gz does not work out of the box, since the build.sh script requires a git repository)
RUN git clone https://github.com/microsoft/onnxruntime src \
  && (cd src && git checkout v1.13.1) \
  && ./src/build.sh \
    --config MinSizeRel \
    --build_shared_lib \
    --build_dir build \
    --use_cuda \
    --cuda_home /usr/local/cuda \
    --cudnn_home /usr/local/cuda \
    --minimal_build \
#    --parallel 1 \
    --skip_tests \
    --cmake_extra_defines \
      CMAKE_INSTALL_PREFIX=${PREFIX} \
      CMAKE_CUDA_ARCHITECTURES=${CUDA_ARCH} \
  && cmake --build build/MinSizeRel -- install \
  && rm -rf build src
