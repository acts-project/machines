# Docker machinery, part of the ACTS project
#
# (c) 2024 CERN for the benefit of the ACTS project
#
# Mozilla Public License Version 2.0

# Start from the (at the time of writing) latest Acts Ubuntu 24.04 image.
# @TODO: Update this
FROM ghcr.io/acts-project/ubuntu2404:68

# Some description for the image.
LABEL description="Ubuntu 24.04 with Acts dependencies and ROCm/HIP + oneAPI"
LABEL maintainer="Stephen Nicholas Swatman <stephen.nicholas.swatman@cern.ch>"
LABEL version="1"

# Set up the ROCm package signing key.
RUN mkdir --parents --mode=0755 /etc/apt/keyrings && \
    curl -SL https://repo.radeon.com/rocm/rocm.gpg.key | \
    gpg --dearmor > /etc/apt/keyrings/rocm.gpg

# Set up the ROCm repository.
COPY rocm.list /etc/apt/sources.list.d/
COPY rocm-pin-600 /etc/apt/preferences.d/

# Install ROCm/HIP.
ARG ROCM_VERSION=6.1.0
RUN apt-get update && \
    apt-get install -y rocm-hip-runtime-dev${ROCM_VERSION} && \
    apt-get clean -y
ENV HIP_PLATFORM=amd

# Set up the Intel package signing key.
RUN curl -SL https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB | \
    gpg --dearmor > /usr/share/keyrings/oneapi-archive-keyring.gpg

# Set up the oneAPI repository.
COPY oneapi.list /etc/apt/sources.list.d/

# Install oneAPI.
ARG ONEAPI_VERSION=2025.0
RUN apt-get update && \
    apt-get install -y intel-oneapi-compiler-dpcpp-cpp-${ONEAPI_VERSION} && \
    apt-get clean -y

# Install the CodePlay AMD plugin on top of oneAPI.
ARG CODEPLAY_PLUGIN_VERSION=2025.0
RUN curl -SL "https://developer.codeplay.com/api/v1/products/download?product=oneapi&variant=amd&version=${CODEPLAY_PLUGIN_VERSION}&filters[]=${ROCM_VERSION}&filters[]=linux" \
    -o plugin.sh && \
    sh plugin.sh --install-dir /opt/intel/oneapi --yes && \
    rm plugin.sh

# Set up the oneAPI environment. Note that one *MUST* source the
# /opt/intel/oneapi/setvars.sh script to make the following work. Which has to
# be done in the respective CI scripts.
ENV CC="clang"
ENV CXX="clang++"
ENV SYCLCXX="clang++"
ENV SYCLFLAGS="-fsycl -fsycl-targets=amd_gpu_gfx1031"
