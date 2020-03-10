FROM ubuntu:19.10

SHELL ["/bin/bash","-c"]

RUN apt-get update && apt-get install -y \
  xz-utils \
  build-essential \
  curl \
  rsync \
  libeigen3-dev \
  libexpat-dev \
  libxerces-c-dev \
  python3 \
  python3-dev \
  python3-pip \
  ninja-build \
  git \
  xsltproc \
  libboost-dev \
  libboost-program-options-dev \
  xorg-dev \
  freeglut3-dev \
  libboost-test-dev \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

## install cmake
ENV CMAKE_VERSION=3.16.3
RUN curl -SL https://github.com/Kitware/CMake/releases/download/v${CMAKE_VERSION}/cmake-${CMAKE_VERSION}-Linux-x86_64.tar.gz \
    | tar -xzC . \
    && mv cmake-* cmake \
    && rsync -rv --links /cmake/ /usr/local/ \
    && rm -rf /cmake

ENV ROOT_VERSION=6.20.00
RUN curl -SL https://root.cern/download/root_v${ROOT_VERSION}.source.tar.gz \
    | tar -xzC . \
    && mv root-* root_src \
    && mkdir root_build && cd root_build \
    && cmake ../root_src \
              -DCMAKE_CXX_STANDARD=17 \
	      -DCMAKE_INSTALL_PREFIX=/usr/local \
	      -Dx11=ON \
              -Dfftw3=ON \
              -Dgdml=ON \
              -Dminuit2=ON \
              -Dopengl=ON \
              -Droofit=ON \
              -Dxml=ON \
    && make -j$(nproc) \
    && make install \
    && rm -rf /root_src /root_build

ENV GEANT4_VERSION=10.6.1
RUN curl -SL https://github.com/Geant4/geant4/archive/v${GEANT4_VERSION}.tar.gz \
    | tar -xzC . \
    && mv geant4-* geant4_src \
    && mkdir geant4_build && cd geant4_build \
    && cmake ../geant4_src \
	 -DGEANT4_USE_GDML=ON \
	 -DGEANT4_BUILD_CXXSTD=17 \
	 -DCMAKE_INSTALL_PREFIX=/usr/local \
    && make -j$(nproc) \
    && make install \
    && rm -rf /geant4_src /geant4_build

RUN source /usr/local/bin/thisroot.sh
ENV LD_LIBRARY_PATH=/usr/local/lib

ENV DD4HEP_VERSION=01-11-02
RUN curl -SL https://github.com/AIDASoft/DD4hep/archive/v${DD4HEP_VERSION}.tar.gz \
    | tar -xzC . \
    && mv DD4hep-* dd4hep_src \
    && mkdir dd4hep_build && cd dd4hep_build \
    && cmake ../dd4hep_src \
	   -DDD4HEP_USE_GEANT4=ON \
	   -DCMAKE_CXX_STANDARD=17 \
	   -DCMAKE_INSTALL_PREFIX=/usr/local \
    && make -j$(nproc) \
    && make install \
    && rm -rf /dd4hep_src /dd4hep_build


CMD [ "/bin/bash" ]
