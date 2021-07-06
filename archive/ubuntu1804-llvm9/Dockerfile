# Check http://releases.llvm.org/download.html#9.0.0 for the latest available binaries
FROM ubuntu:18.04

SHELL ["/bin/bash","-c"]

RUN apt-get update && apt-get install -y \
  xz-utils \
  build-essential \
  curl \
  rsync \
  libeigen3-dev \
  libexpat-dev \
  libxerces-c-dev \
  python \
  python-dev \
  ninja-build \
  git \
  xsltproc \
  && rm -rf /var/lib/apt/lists/*

# install clang
ENV LLVM_VERSION=9.0.1
RUN curl -SL https://github.com/llvm/llvm-project/releases/download/llvmorg-${LLVM_VERSION}/clang+llvm-${LLVM_VERSION}-x86_64-linux-gnu-ubuntu-16.04.tar.xz \
  | tar -xJC . \
  && mv clang+llvm-* clang+llvm \
  && rsync -rv --links /clang+llvm/ /usr/local/ && rm -rf /clang+llvm

## install cmake
ENV CMAKE_VERSION=3.16.3
RUN curl -SL https://github.com/Kitware/CMake/releases/download/v${CMAKE_VERSION}/cmake-${CMAKE_VERSION}-Linux-x86_64.tar.gz \
    | tar -xzC . \
    && mv cmake-* cmake \
    && rsync -rv --links /cmake/ /usr/local/ && rm -rf /cmake

ENV CXX=clang++ CC=clang

# boost
ENV BOOST_VERSION=1.72.0
RUN export BOOST_VERSION_=${BOOST_VERSION//./_} && \
    curl -SL boost-${BOOST_VERSION_}.tar.gz https://boostorg.jfrog.io/artifactory/main/release/${BOOST_VERSION}/source/boost_{BOOST_VERSION_}.tar.gz \
    | tar -xzC . && \
    cd boost_${BOOST_VERSION_}/ && \
    ./bootstrap.sh --prefix=/usr/local/ --with-toolset=clang --with-libraries=program_options,test && \
    ./b2 clean && \
    ./b2 toolset=clang cxxflags="-std=c++17 -stdlib=libc++" linkflags="-stdlib=libc++" --prefix=/usr/local -j $(nproc) stage release && \
    ./b2 install toolset=clang cxxflags="-std=c++17 -stdlib=libc++" linkflags="-stdlib=libc++" --prefix=/usr/local && \
    cd .. && rm -r boost_${BOOST_VERSION_}

ENV LD_LIBRARY_PATH=/usr/local/lib
#RUN curl -SL https://root.cern/download/root_v6.16.00.source.tar.gz \
    #| tar -xzC .
#RUN mkdir root_build && cd root_build \
    #&& cmake ../root-6.16.00 \
         #-DCMAKE_BUILD_TYPE="Release" \
         #-DCMAKE_CXX_COMPILER="clang++" \
         #-DCMAKE_CXX_FLAGS="-march=native" \
         #-DCMAKE_CXX_STANDARD="17" \
         #-DCMAKE_C_COMPILER="clang" \
         #-DCMAKE_C_FLAGS="-march=native" \
         #-DCMAKE_INSTALL_PREFIX=/usr/local \
         #-Dasimage="OFF" \
         #-Dastiff="OFF" \
         #-Dbuiltin_afterimage="OFF" \
         #-Dbuiltin_ftgl="OFF" \
         #-Dbuiltin_glew="OFF" \
         #-Dclad="OFF" \
         #-Ddavix="OFF" \
         #-Dfftw3="OFF" \
         #-Dfitsio="OFF" \
         #-Dimt="OFF" \
         #-Dlibcxx="ON" \
         #-Dmysql="OFF" \
         #-Dopengl="OFF" \
         #-Doracle="OFF" \
         #-Dpgsql="OFF" \
         #-Dpythia6="OFF" \
         #-Dpythia8="OFF" \
         #-Dpython="OFF"\
         #-Droofit="OFF" \
         #-Droot7="OFF" \
         #-Dsqlite="OFF" \
         #-Dtmva="OFF" \
         #-Dtmva-cpu="OFF" \
         #-Dtmva-gpu="OFF" \
         #-Dtmva-pymva="OFF" \
         #-Dvc="OFF" \
         #-Dvdt="OFF" \
         #-Dx11="OFF" \
         #-Dxft="OFF" \
         #-Dxrootd="OFF" \
   #&& make -j$(nproc)

# root deps
#RUN apt-get update && apt-get -y install \
      #libfftw3-dev \
      #libgsl-dev \
      #libx11-dev \
      #libxext-dev \
      #libxft-dev \
      #libxml2-dev \
      #libxpm-dev \
      #python-dev \
      #xlibmesa-glu-dev \
      #git \
  #&& rm -rf /var/lib/apt/lists/*

#RUN curl -SL https://root.cern/download/root_v6.16.00.source.tar.gz \
    #| tar -xzC .
#RUN mkdir root_build && cd root_build \
    #&& cmake ../root-6.16.00 \
              #-Dcxx17=ON \
          #-Dlibcxx=ON \
	  #-Dfftw3=ON \
	  #-Dgdml=ON \
	  #-Dminuit2=ON \
	  #-Dopengl=ON \
	  #-Droofit=ON \
	  #-Dxml=ON \
    #&& make -j$(nproc) \
    #&& make install

#RUN curl -SL https://root.cern/download/root_v6.16.00.Linux-ubuntu18-x86_64-gcc7.3.tar.gz | tar -xzC .
#RUN rsync -rv --links /root/ /usr/local/ && rm -rf /root

#RUN ["/bin/bash", "-c", "source /root/bin/thisroot.sh && echo $CMAKE_PREFIX_PATH"]


#RUN curl -SL http://geant4-data.web.cern.ch/geant4-data/releases/geant4.10.05.tar.gz | tar -xzC .
#RUN mkdir /geant4_build && cd /geant4_build \
    #&& cmake ../geant4.10.05 \
         #-DGEANT4_USE_GDML=ON \
         #-DGEANT4_BUILD_CXXSTD=17 \
         #-DCMAKE_CXX_FLAGS="-stdlib=libc++" \
    #&& make -j$(nproc) \
    #&& make install


#RUN curl -SL https://github.com/AIDASoft/DD4hep/archive/v01-10.tar.gz | tar -xzC .
#RUN mkdir /dd4hep_build && cd /dd4hep_build \
    #&& cmake ../DD4hep-01-10 \
           #-DDD4HEP_USE_GEANT4=ON \
           #-DCMAKE_CXX_STANDARD=17 \
           #-DCMAKE_INSTALL_PREFIX=/usr/local \
           #-DCMAKE_CXX_FLAGS="-stdlib=libc++" \
    #&& make -j$(nproc) \
    #&& make install


# Start from a Bash prompt
CMD [ "/bin/bash" ]
