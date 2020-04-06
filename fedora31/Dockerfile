FROM fedora:31

LABEL description="Fedora 31 with Acts dependencies"
LABEL maintainer="Moritz Kiehn <msmk@cern.ch>"
# increase whenever any of the RUN commands change
LABEL version="2"

# install dependencies from the package manager
#
# intentionally do not run `dnf upgrade`. assume that the base image
# is sufficienty up-to-date and avoid adding unnecessary changes.
#
# ROOT is available as a system package, but has problems when compiling
# with C++17. ROOT must be installed manually.
# see also https://root.cern.ch/build-prerequisites
RUN dnf install --assumeyes \
    @development-tools \
    boost-devel \
    cmake \
    curl \
    doxygen \
    eigen3-devel \
    expat-devel \
    freeglut-devel \
    ftgl-devel \
    git \
    glew-devel \
    gl2ps-devel \
    gsl-devel \
    HepMC3-devel \
    libX11-devel \
    libXext-devel \
    libXft-devel \
    libXpm-devel \
    libzstd-devel \
    lz4-devel \
    ninja-build \
    openssl-devel \
    pcre-devel \
    pythia8-devel \
    python3-breathe \
    python3-devel \
    python3-numpy \
    python3-pip \
    python3-root \
    python3-sphinx \
    tbb-devel \
    xerces-c-devel \
    xxhash-devel \
    xz-devel \
    zlib-devel \
  && dnf clean all --assumeyes

# manual builds for hep-specific packages
ENV GET curl --location --silent --create-dirs
ENV UNPACK_TO_SRC tar -xz --strip-components=1 --directory src
ENV PREFIX /usr/local

# Geant4
RUN mkdir src \
  && ${GET} https://geant4-data.web.cern.ch/geant4-data/releases/geant4.10.06.p01.tar.gz \
    | ${UNPACK_TO_SRC} \
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

# ROOT
RUN mkdir src \
  && ${GET} https://root.cern/download/root_v6.20.04.source.tar.gz \
    | ${UNPACK_TO_SRC} \
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
RUN mkdir src \
  && ${GET} https://github.com/AIDASoft/DD4hep/archive/v01-11-02.tar.gz \
    | ${UNPACK_TO_SRC} \
  && cmake -B build -S src -GNinja \
    -DCMAKE_INSTALL_PREFIX=${PREFIX} \
    -DBUILD_DOCS=OFF \
    -DBUILD_TESTING=OFF \
    -DDD4HEP_IGNORE_GEANT4_TLS=ON \
    -DDD4HEP_USE_GEANT4=ON \
    -DDD4HEP_USE_XERCESC=ON \
  && cmake --build build -- install \
  && rm -rf build src

