# Docker machinery, part of the ACTS project
#
# (c) 2024 CERN for the benefit of the ACTS project
#
# Mozilla Public License Version 2.0

FROM rocm/dev-ubuntu-22.04:6.1

LABEL description="Ubuntu 22.04 with Acts dependencies and ROCm using clang, built using C++20"
LABEL maintainer="Paul Gessinger <paul.gessinger@cern.ch>"
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
    clang \
    curl \
    git \
    git-lfs \
    freeglut3-dev \
    libboost-dev \
    libboost-filesystem-dev \
    libboost-program-options-dev \
    libboost-test-dev \
    libeigen3-dev \
    libexpat-dev \
    libftgl-dev \
    libgl2ps-dev \
    libglew-dev \
    libgsl-dev \
    liblz4-dev \
    liblzma-dev \
    libpcre3-dev \
    libssl-dev \
    libtbb-dev \
    libx11-dev \
    libxext-dev \
    libxft-dev \
    libxpm-dev \
    libxerces-c-dev \
    libxxhash-dev \
    libzstd-dev \
    ninja-build \
    python3 \
    python3-dev \
    python3-pip \
    rsync \
    zlib1g-dev \
    ccache \
  && apt-get remove -y gcc g++ \
  && apt-get clean -y

# manual builds for hep-specific packages
ENV GET curl --location --silent --create-dirs
ENV UNPACK_TO_SRC tar -xz --strip-components=1 --directory src
ENV PREFIX /usr/local

# use clang by default
ENV CC clang
ENV CXX clang++

# manually install CMake
RUN apt-get purge -y cmake
RUN mkdir src \
  && ${GET} https://github.com/Kitware/CMake/releases/download/v3.30.1/cmake-3.30.1.tar.gz \
    | ${UNPACK_TO_SRC} \
  && ( \
    cd src \
    && ./configure \
    && make -j $(nproc) \
    && make install \
  ) \
  && rm -rf src
