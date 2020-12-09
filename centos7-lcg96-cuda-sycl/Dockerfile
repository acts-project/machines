# See https://gitlab.cern.ch/akraszna/atlas-gpu-devel-env/-/blob/master/Dockerfile
FROM nvidia/cuda:10.1-devel-centos7

LABEL description="CERN CentOS 7 with Acts dependencies from LCG 96"
LABEL maintainer="Paul Gessinger <paul.gessinger@cern.ch>"
# increase whenever any of the RUN commands change
LABEL version="1"


# Put the repository configuration file(s) in place.
COPY docker/*.repo /etc/yum.repos.d/

# Install a modern compiler, and some basic packages necessary for ATLAS
# offline software development.
RUN yum -y install which redhat-lsb-core nano sudo glibc-devel libaio         \
           libX11 libXft libXpm libXext libXi libSM mesa-libGL mesa-libGLU    \
           gcc_8.3.0_x86_64_centos7-3.0.0-1.noarch                            \
           binutils_2.30_x86_64_centos7 git wget tar                          \
           atlas-devel ctags libX11-devel libXpm-devel libXft-devel           \
           libXext-devel libXi-devel openssl-devel rpm-build gmp-devel        \
           mesa-libGL-devel mesa-libGLU-devel libcurl-devel glib2-devel       \
           xz-devel rpm-build &&                                              \
    yum clean all &&                                                          \
    wget https://cmake.org/files/v3.17/cmake-3.17.3-Linux-x86_64.tar.gz &&    \
    mkdir -p /opt/cmake/3.17.3/Linux-x86_64 &&                                \
    tar -C /opt/cmake/3.17.3/Linux-x86_64 --strip-components=1                \
        --no-same-owner -xvf cmake-*-Linux-x86_64.tar.gz &&                   \
    rm cmake-*-Linux-x86_64.tar.gz &&                                         \
    ln -s /opt/cmake/*/Linux-x86_64/bin/* /usr/local/bin/ &&                  \
    wget https://github.com/ninja-build/ninja/releases/download/v1.10.0/ninja-linux.zip && \
    mkdir -p /opt/ninja/1.10.0/Linux-x86_64 &&                                \
    unzip ninja-linux.zip -d /opt/ninja/1.10.0/Linux-x86_64 &&                \
    chmod 755 /opt/ninja/*/Linux-x86_64/ninja &&                              \
    ln -s /opt/ninja/*/Linux-x86_64/ninja /usr/local/bin/ &&                  \
    rm ninja-linux.zip

# Build a particular version of Intel's Clang compiler.
ARG LLVM_VERSION=55eef6c
ARG LLVM_INSTALL_DIR=/opt/intel-clang/11.0.0-${LLVM_VERSION}/x86_64-centos7
ARG LLVM_SOURCE_DIR=/root/llvm
ARG LLVM_BINARY_DIR=/root/build
ARG CUDA_DRIVER_DIR=/root/cuda
ARG GCC_INSTALL_DIR=/opt/lcg/gcc/8.3.0/x86_64-centos7
COPY cuda/libcuda.so.* ${CUDA_DRIVER_DIR}/
RUN ln -s libcuda.so.440.44 ${CUDA_DRIVER_DIR}/libcuda.so.1                   \
    && ln -s libcuda.so.1 ${CUDA_DRIVER_DIR}/libcuda.so                       \
    && git clone https://github.com/intel/llvm.git ${LLVM_SOURCE_DIR}         \
    && cd ${LLVM_SOURCE_DIR}/ && git checkout ${LLVM_VERSION}                 \
    && mkdir -p ${LLVM_BINARY_DIR} && cd ${LLVM_BINARY_DIR}/                  \
    && source ${GCC_INSTALL_DIR}/setup.sh                                     \
    && cmake -DCMAKE_BUILD_TYPE=Release                                       \
       -DCMAKE_INSTALL_PREFIX=${LLVM_INSTALL_DIR}                             \
       -DLLVM_TARGETS_TO_BUILD="X86;NVPTX"                                    \
       -DLLVM_EXTERNAL_PROJECTS="llvm-spirv;sycl;libdevice"                   \
       -DLLVM_ENABLE_PROJECTS="clang;clang-tools-extra;compiler-rt;lld;llvm-spirv;sycl;libclc" \
       -DLLVM_EXTERNAL_LLVM_SPIRV_SOURCE_DIR=${LLVM_SOURCE_DIR}/llvm-spirv    \
       -DLLVM_EXTERNAL_SYCL_SOURCE_DIR=${LLVM_SOURCE_DIR}/sycl                \
       -DLLVM_EXTERNAL_LIBDEVICE_SOURCE_DIR=${LLVM_SOURCE_DIR}/libdevice      \
       -DLLVM_ENABLE_EH=ON -DLLVM_ENABLE_PIC=ON -DLLVM_ENABLE_RTTI=ON         \
       -DSYCL_BUILD_PI_CUDA=ON                                                \
       -DLIBCLC_TARGETS_TO_BUILD="nvptx64--;nvptx64--nvidiacl"                \
       -DCUDA_TOOLKIT_ROOT_DIR=/usr/local/cuda                                \
       -DCMAKE_PREFIX_PATH=${CUDA_DRIVER_DIR}                                 \
       -DOpenCL_INCLUDE_DIRS= -DOpenCL_LIBRARIES=                             \
       -DOpenCL_INSTALL_KHRONOS_ICD_LOADER=TRUE                               \
       -DGCC_INSTALL_PREFIX=${GCC_INSTALL_DIR}                                \
       ${LLVM_SOURCE_DIR}/llvm/                                               \
    && export MAKEFLAGS="-j`nproc` -l`nproc`"                                 \
    && make && make libsycldevice && make install                             \
    && rm -rf ${LLVM_SOURCE_DIR} ${LLVM_BINARY_DIR} ${CUDA_DRIVER_DIR}        \
    && ln -s 11.0.0-${LLVM_VERSION} /opt/intel-clang/11.0.0
COPY docker/setup.sh ${LLVM_INSTALL_DIR}/


ENV LCG_RELEASE 97
ENV LCG_PLATFORM_BASE x86_64-centos7
ENV LCG_PLATFORM ${LCG_PLATFORM_BASE}-gcc8-opt
# branch/tag/commit reference for lcgcmake. we need a specific version
# to be able to create an RPM-based view.
ENV LCGCMAKE_REF 16176752

# Add the LCG rpm repository as described here
#
#     https://lcgpackages.web.cern.ch
#
# and use it to install all explicit Acts dependencies from an LCG release.
RUN yum -y install \
    LCG_${LCG_RELEASE}_Boost_1.70.0_${LCG_PLATFORM//-/_}.noarch \
    LCG_${LCG_RELEASE}_CMake_3.14.3_${LCG_PLATFORM//-/_}.noarch \
    LCG_${LCG_RELEASE}_DD4hep_01_10_${LCG_PLATFORM//-/_}.noarch \
    LCG_${LCG_RELEASE}_eigen_3.3.7_${LCG_PLATFORM//-/_}.noarch \
    LCG_${LCG_RELEASE}_Geant4_10.05.p01_${LCG_PLATFORM//-/_}.noarch \
    LCG_${LCG_RELEASE}_hepmc3_3.1.1_${LCG_PLATFORM//-/_}.noarch \
    LCG_${LCG_RELEASE}_ninja_1.9.0_${LCG_PLATFORM//-/_}.noarch \
    LCG_${LCG_RELEASE}_pythia8_240_${LCG_PLATFORM//-/_}.noarch \
    LCG_${LCG_RELEASE}_ROOT_6.18.00_${LCG_PLATFORM//-/_}.noarch \
    LCG_${LCG_RELEASE}_tbb_2019_U7_${LCG_PLATFORM//-/_}.noarch \
  && yum -y clean all

# Add missing directory link so the view creating script finds the compiler
RUN ln -rsv /opt/lcg/gcc/8.2.0-3fa06 /opt/lcg/gcc/8
# Bugfix for broken setup script
ADD fixed-gcc-setup.sh /opt/lcg/gcc/8.2.0-3fa06/x86_64-centos7/setup.sh

# Create the LCG view. Use a fixed location since there is only one
# release/platform combination. This way, images with different
# configurations (including different compilers) can be easily substituted
# without needing to know the specific contents.
RUN git clone https://gitlab.cern.ch/sft/lcgcmake.git lcgcmake \
  && (cd lcgcmake; git checkout ${LCGCMAKE_REF}) \
  && lcgcmake/cmake/scripts/create_lcg_view.py -v \
    -l /opt/lcg/LCG_${LCG_RELEASE} \
    -p ${LCG_PLATFORM} \
    /opt/lcg_view \
  && rm -rf lcgcmake
