FROM ubuntu:20.04

LABEL description="Ubuntu 20.04 with Acts dependencies"
LABEL maintainer="Paul Gessinger <paul.gessinger@cern.ch>"
# increase whenever any of the RUN commands change
LABEL version="1"

# DEBIAN_FRONTEND ensures non-blocking operation (tzdata is a problem)
ENV DEBIAN_FRONTEND noninteractive

# Get the packages necessary to set up the Intel repository.
RUN apt-get update -y \
  && apt-get install -y gnupg2 curl \
  && apt-get clean -y

# Set up the Intel package repository.
RUN curl https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB | apt-key add - \
  && echo "deb https://apt.repos.intel.com/oneapi all main" > /etc/apt/sources.list.d/oneAPI.list

# Install the oneAPI compiler.
RUN apt-get update -y \
  && apt-get install -y \
    intel-oneapi-compiler-dpcpp-cpp-2022.0.2 \
  && apt-get clean -y

# Set up the environment variables compelling CMake to use the Intel compilers.
ENV CC icx
ENV CXX icpx
ENV SYCLCXX dpcpp

# Install all packages needed by the Acts projects, and the other externals
# built by hand.
RUN apt-get update -y \
  && apt-get install -y \
    libstdc++-9-dev \
    binutils \
    make \
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
  && apt-get remove --purge -y gcc-9 \
  && apt-get autoremove -y \
  && apt-get clean -y

# manual builds for hep-specific packages
ENV GET curl --location --silent --create-dirs
ENV UNPACK_TO_SRC tar -xz --strip-components=1 --directory src
ENV PREFIX /usr/local

# CMake 3.16.3 version in APT is too old
# requires rsync; installation uses `rsync` instead of `install`
RUN mkdir src \
  && ${GET} https://github.com/Kitware/CMake/releases/download/v3.21.2/cmake-3.21.2-Linux-x86_64.tar.gz \
    | ${UNPACK_TO_SRC} \
  && rsync -ruv src/ ${PREFIX} \
  && cd .. \
  && rm -rf src

# Geant4
RUN mkdir src \
  && ${GET} https://geant4-data.web.cern.ch/releases/geant4.10.06.p01.tar.gz \
    | ${UNPACK_TO_SRC} \
  && . /opt/intel/oneapi/setvars.sh \
  && cmake -B build -S src -GNinja \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=${PREFIX} \
    -DGEANT4_BUILD_CXXSTD=17 \
    -DGEANT4_INSTALL_DATA=OFF \
    -DGEANT4_USE_GDML=ON \
    -DGEANT4_USE_SYSTEM_EXPAT=ON \
    -DGEANT4_USE_SYSTEM_ZLIB=ON \
  && cmake --build build -- install \
  && rm -rf build src

# HepMC3
RUN mkdir src \
  && ${GET} https://hepmc.web.cern.ch/hepmc/releases/HepMC3-3.2.1.tar.gz \
    | ${UNPACK_TO_SRC} \
  && . /opt/intel/oneapi/setvars.sh \
  && cmake -B build -S src -GNinja \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=${PREFIX} \
    -DHEPMC3_BUILD_STATIC_LIBS=OFF \
    -DHEPMC3_ENABLE_PYTHON=OFF \
    -DHEPMC3_ENABLE_ROOTIO=OFF \
    -DHEPMC3_ENABLE_SEARCH=OFF \
  && cmake --build build -- install \
  && rm -rf build src

# Pythia8
# requires rsync; installation uses `rsync` instead of `install`
RUN mkdir src \
  && ${GET} https://pythia.org/download/pythia82/pythia8244.tgz\
    | ${UNPACK_TO_SRC} \
  && cd src \
  && . /opt/intel/oneapi/setvars.sh \
  && ./configure --enable-shared --prefix=${PREFIX} \
  && make -j$(nproc) install \
  && cd .. \
  && rm -rf src

# nlohmann's JSON
RUN mkdir src \
  && ${GET} https://github.com/nlohmann/json/archive/refs/tags/v3.10.2.tar.gz \
    | ${UNPACK_TO_SRC} \
  && . /opt/intel/oneapi/setvars.sh \
  && cmake -B build -S src -GNinja \
  && cmake --build build -- install \
  && rm -rf build src

# ROOT
RUN mkdir src \
  && ${GET} https://root.cern/download/root_v6.24.06.source.tar.gz \
    | ${UNPACK_TO_SRC} \
  && . /opt/intel/oneapi/setvars.sh \
  && cmake -B build -S src -GNinja \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_CXX_STANDARD=17 \
    -DCMAKE_INSTALL_PREFIX=${PREFIX} \
    -Dfail-on-missing=ON \
    -Dgminimal=ON \
    -Dgdml=ON \
    -Dopengl=ON \
    -Dpyroot=ON \
  && cmake --build build -- install \
  && rm -rf build src

# DD4hep
# requires Geant4 and ROOT and must come last
#
# environment variables needed for DD4hep to find ROOT libraries
ENV LD_LIBRARY_PATH /usr/local/lib
ENV PYTHON_PATH /usr/local/lib
RUN mkdir src \
  && ${GET} https://github.com/AIDASoft/DD4hep/archive/v01-17.tar.gz \
    | ${UNPACK_TO_SRC} \
  && . /opt/intel/oneapi/setvars.sh \
  && cmake -B build -S src -GNinja \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_CXX_STANDARD=17 \
    -DCMAKE_INSTALL_PREFIX=${PREFIX} \
    -DCMAKE_PREFIX_PATH=${PREFIX} \
    -DBUILD_TESTING=OFF \
    -DDD4HEP_BUILD_PACKAGES="DDG4 DDDetectors DDRec" \
    -DDD4HEP_IGNORE_GEANT4_TLS=ON \
    -DDD4HEP_USE_GEANT4=ON \
    -DDD4HEP_USE_XERCESC=ON \
  && cmake --build build -- install \
  && rm -rf build src
