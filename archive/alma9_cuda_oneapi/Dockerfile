# Docker machinery, part of the ACTS project
#
# (c) 2024 CERN for the benefit of the ACTS project
#
# Mozilla Public License Version 2.0

FROM cern/alma9-base:latest

LABEL description="CERN AlmaLinux 9 with Acts dependencies and CUDA + oneAPI"
LABEL version="2"
ARG CACHEBUST=0

RUN dnf install -y https://linuxsoft.cern.ch/wlcg/el9/x86_64/HEP_OSlibs-9.1.0-2.el9.x86_64.rpm \
  && dnf -y clean all

# Set up gcc 13.
RUN dnf install -y gcc-toolset-13

# Install boost development package
RUN dnf install -y boost boost-devel

# Set up the CUDA repository.
COPY cuda.repo /etc/yum.repos.d/cuda.repo
ARG CUDA_VERSION=12-6

# Install CUDA
RUN dnf install -y cuda-${CUDA_VERSION}.x86_64

# Set up the oneAPI repository.
COPY oneapi.repo /etc/yum.repos.d/oneapi.repo

# Install oneAPI.
ARG ONEAPI_VERSION=2025.0
RUN dnf install -y intel-oneapi-compiler-dpcpp-cpp-${ONEAPI_VERSION}

# Install the CodePlay AMD plugin on top of oneAPI.
ARG CODEPLAY_PLUGIN_VERSION=2025.0
RUN curl -SL \
    "https://developer.codeplay.com/api/v1/products/download?product=oneapi&variant=nvidia&filters[]=linux&version=${CODEPLAY_PLUGIN_VERSION}" \
    -o plugin.sh && \
    sh plugin.sh --install-dir /opt/intel/oneapi --yes && \
    rm plugin.sh

# By default the environment with ROCm, OneAPI SYCL compiler, and AMD backend plugin is loaded
ADD --chmod=700 setenv.sh /
# Make sure it's executable
RUN chmod +x /setenv.sh
ENTRYPOINT /setenv.sh
