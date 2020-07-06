FROM ubuntu:19.10

LABEL description="Ubuntu 19.10 with Acts dependencies"
LABEL maintainer="Paul Gessinger <paul.gessinger@cern.ch>"
# increase whenever any of the RUN commands change
LABEL version="1"

# install system dependencies
#
# see also https://root.cern.ch/build-prerequisites
# DEBIAN_FRONTEND ensures non-blocking operation (tzdata is a problem)
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get -y update \
  && apt-get -y install \
    build-essential \
    cmake \
    curl \
    doxygen \
    git \
    libboost-dev \
    libboost-filesystem-dev \
    libboost-program-options-dev \
    libboost-test-dev \
    libeigen3-dev \
    libexpat-dev \
    libfftw3-dev \
    libjpeg-dev \
    libpng-dev \
    libtbb-dev \
    libx11-dev \
    libxext-dev \
    libxft-dev \
    libxpm-dev \
    libxerces-c-dev \
    ninja-build \
    python3 \
    python3-dev \
    python3-pip \
    rsync \
    zlib1g-dev \
  && apt-get -y clean

# install external dependencies
ENV GET curl --location --silent --create-dirs --output
ENV PREFIX /usr/local

# ROOT
RUN ${GET} src/root.tar.gz \
    https://root.cern/download/root_v6.20.04.source.tar.gz \
  && tar -xf src/root.tar.gz --strip-components=1 --directory src \
  && cmake -B build -S src -GNinja \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_CXX_STANDARD=17 \
    -DCMAKE_INSTALL_PREFIX=${PREFIX} \
    -Dfftw3=ON \
    -Dgdml=ON \
    -Dminuit2=ON \
    -Dopengl=ON \
    -Droofit=ON \
    -Dx11=ON \
    -Dxml=ON \
  && cmake --build build -- install \
  && rm -rf build src

# HepMC3
RUN ${GET} src/hepmc3.tar.gz \
    https://hepmc.web.cern.ch/hepmc/releases/HepMC3-3.2.1.tar.gz \
  && tar -xf src/hepmc3.tar.gz --strip-components=1 --directory src \
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
RUN ${GET} src/pythia8.tar.gz \
    http://home.thep.lu.se/~torbjorn/pythia8/pythia8244.tgz \
  && cd src \
  && tar -xf pythia8.tar.gz --strip-components=1 \
  && ./configure --enable-shared --with-hepmc3=${PREFIX} \
  && make install \
  && cd .. \
  && rm -rf src

# Geant4
RUN ${GET} src/geant4.tar.gz \
    https://geant4-data.web.cern.ch/geant4-data/releases/geant4.10.06.p01.tar.gz \
  && tar -xf src/geant4.tar.gz --strip-components=1 --directory src \
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

# DD4hep
#RUN ${GET} src/dd4hep.tar.gz \
#    https://github.com/AIDASoft/DD4hep/archive/v01-11-02.tar.gz \
#  && tar -xf src/dd4hep.tar.gz --strip-components=1 --directory src \
#  && cmake -B build -S src -GNinja \
#    -DCMAKE_BUILD_TYPE=Release \
#    -DCMAKE_INSTALL_PREFIX=${PREFIX} \
#    -DCMAKE_PREFIX_PATH=${PREFIX} \
#    -DBUILD_TESTING=OFF \
#    -DDD4HEP_IGNORE_GEANT4_TLS=ON \
#    -DDD4HEP_USE_GEANT4=ON \
#    -DDD4HEP_USE_XERCESC=ON \
#  && cmake --build build -- install \
#  && rm -rf build src

