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

# Geant4
RUN mkdir src \
  && ${GET} https://gitlab.cern.ch/geant4/geant4/-/archive/v11.1.1/geant4-v11.1.1.tar.gz \
    | ${UNPACK_TO_SRC} \
  && cmake -B build -S src -GNinja \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=${PREFIX} \
    -DCMAKE_CXX_STANDARD=20 \
    -DGEANT4_BUILD_TLS_MODEL=global-dynamic \
    -DGEANT4_INSTALL_DATA=OFF \
    -DGEANT4_USE_GDML=ON \
    -DGEANT4_USE_SYSTEM_EXPAT=ON \
    -DGEANT4_USE_SYSTEM_ZLIB=ON \
    -DGEANT4_INSTALL_PACKAGE_CACHE=OFF \
  && cmake --build build -- -j $(nproc) install \
  && rm -rf build src

# HepMC3
RUN mkdir src \
  && ${GET} https://gitlab.cern.ch/hepmc/HepMC3/-/archive/3.2.5/HepMC3-3.2.5.tar.gz \
    | ${UNPACK_TO_SRC} \
  && cmake -B build -S src -GNinja \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=${PREFIX} \
    -DHEPMC3_BUILD_STATIC_LIBS=OFF \
    -DHEPMC3_ENABLE_PYTHON=OFF \
    -DHEPMC3_ENABLE_ROOTIO=OFF \
    -DHEPMC3_ENABLE_SEARCH=OFF \
  && cmake --build build -- -j $(nproc) install \
  && rm -rf build src

# Pythia8
# requires rsync; installation uses `rsync` instead of `install`
RUN mkdir src \
  && ${GET} https://pythia.org/download/pythia83/pythia8309.tgz\
    | ${UNPACK_TO_SRC} \
  && cd src \
  && ./configure --enable-shared --prefix=${PREFIX} \
  && make -j$(nproc) install \
  && cd .. \
  && rm -rf src

# nlohmann's JSON
RUN mkdir src \
  && ${GET} https://github.com/nlohmann/json/archive/refs/tags/v3.11.2.tar.gz \
    | ${UNPACK_TO_SRC} \
  && cmake -B build -S src -GNinja \
    -DJSON_BuildTests=OFF \
  && cmake --build build -- -j $(nproc) install \
  && rm -rf build src

# ROOT
RUN mkdir src \
  && ${GET} https://root.cern/download/root_v6.28.06.source.tar.gz \
    | ${UNPACK_TO_SRC} \
  && cmake -B build -S src -GNinja \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=${PREFIX} \
    -DCMAKE_CXX_STANDARD=20 \
    -Dfail-on-missing=ON \
    -Dgminimal=ON \
    -Dgdml=ON \
    -Dopengl=ON \
    -Dpyroot=ON \
    -Droot7=ON \
  && cmake --build build -- -j $(nproc) install \
  && rm -rf build src

# environment variables needed to find ROOT libraries
ENV LD_LIBRARY_PATH /usr/local/lib
ENV PYTHON_PATH /usr/local/lib

# podio
RUN mkdir src \
  && ${GET} https://github.com/AIDASoft/podio/archive/refs/tags/v01-00-01.tar.gz \
    | ${UNPACK_TO_SRC} \
  && cmake -B build -S src -GNinja \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=${PREFIX} \
    -DBUILD_TESTING=OFF \
    -USE_EXTERNAL_CATCH2=OFF \
  && cmake --build build -- -j $(nproc) install \
  && rm -rf build src

# EDM4hep
RUN pip3 install jinja2 pyyaml \
  && mkdir src \
  && ${GET} https://github.com/key4hep/EDM4hep/archive/refs/tags/v00-10-05.tar.gz \
    | ${UNPACK_TO_SRC} \
  && cmake -B build -S src -GNinja \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=${PREFIX} \
    -DBUILD_TESTING=OFF \
    -DUSE_EXTERNAL_CATCH2=OFF \
  && cmake --build build -- -j $(nproc) install \
  && rm -rf build src

# DD4hep
# requires Geant4 and ROOT and must come last
ADD 0001-CMake-allow-finding-newer-versions-of-podio.patch .
RUN mkdir src \
  && ${GET} https://github.com/AIDASoft/DD4hep/archive/v01-29.tar.gz \
    | ${UNPACK_TO_SRC} \
  && patch -p1 -d src < 0001-CMake-allow-finding-newer-versions-of-podio.patch \
  && cmake -B build -S src -GNinja \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_CXX_STANDARD=20 \
    -DCMAKE_INSTALL_PREFIX=${PREFIX} \
    -DCMAKE_PREFIX_PATH=${PREFIX} \
    -DBUILD_TESTING=OFF \
    -DDD4HEP_BUILD_PACKAGES="DDG4 DDDetectors DDRec UtilityApps" \
    -DDD4HEP_IGNORE_GEANT4_TLS=ON \
    -DDD4HEP_USE_GEANT4=ON \
    -DDD4HEP_USE_XERCESC=ON \
    -DDD4HEP_USE_EDM4HEP=ON \
  && cmake --build build -- -j $(nproc) install \
  && rm -rf build src

COPY download_geant4_data.sh /usr/local/bin
