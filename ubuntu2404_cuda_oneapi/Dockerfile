# Docker machinery, part of the ACTS project
#
# (c) 2024 CERN for the benefit of the ACTS project
#
# Mozilla Public License Version 2.0

# Start from the (at the time of writing) latest Acts Ubuntu 24.04 image.
# @TODO: Update this
FROM ghcr.io/acts-project/ubuntu2404:53

# Some description for the image.
LABEL description="Ubuntu 24.04 with Acts dependencies and CUDA + oneAPI"
LABEL maintainer="Stephen Nicholas Swatman <stephen.nicholas.swatman@cern.ch>"

# Add the Ubuntu 24.04 CUDA repository.
RUN curl -SL https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2404/x86_64/cuda-keyring_1.1-1_all.deb \
       -o cuda-keyring.deb && \
    dpkg -i cuda-keyring.deb && \
    rm cuda-keyring.deb

# Install CUDA.
ARG CUDA_VERSION=12-5
RUN apt-get update && \
    apt-get install -y cuda-compat-${CUDA_VERSION} cuda-cudart-${CUDA_VERSION} \
                       cuda-libraries-dev-${CUDA_VERSION}                      \
                       cuda-command-line-tools-${CUDA_VERSION}                 \
                       cuda-minimal-build-${CUDA_VERSION} &&                   \
    apt-get clean -y

# Set up the CUDA environment.
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility
ENV PATH=/usr/local/cuda/bin:${PATH}
ENV LD_LIBRARY_PATH=/usr/local/cuda/lib64:${LD_LIBRARY_PATH}
ENV CUDAHOSTCXX="clang++"
ENV CUDAFLAGS="-allow-unsupported-compiler"

# Set up the Intel package signing key.
RUN mkdir --parents --mode=0755 /etc/apt/keyrings && \
    curl -SL https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB | \
    gpg --dearmor > /usr/share/keyrings/oneapi-archive-keyring.gpg

# Set up the oneAPI repository.
COPY oneapi.list /etc/apt/sources.list.d/

# Install oneAPI.
ARG ONEAPI_VERSION=2024.2
RUN apt-get update && \
    apt-get install -y intel-oneapi-compiler-dpcpp-cpp-${ONEAPI_VERSION} && \
    apt-get clean -y

# Install the CodePlay NVIDIA plugin on top of oneAPI.
ARG CODEPLAY_PLUGIN_VERSION=2024.2
RUN curl -SL \
    "https://developer.codeplay.com/api/v1/products/download?product=oneapi&variant=nvidia&version=${CODEPLAY_PLUGIN_VERSION}" \
    -o plugin.sh && \
    sh plugin.sh --install-dir /opt/intel/oneapi --yes && \
    rm plugin.sh

# Set up the oneAPI environment. Note that one *MUST* source the
# /opt/intel/oneapi/setvars.sh script to make the following work. Which has to
# be done in the respective CI scripts.
ENV CC="clang"
ENV CXX="clang++"
ENV SYCLCXX="clang++"
ENV SYCLFLAGS="-fsycl -fsycl-targets=nvidia_gpu_sm_75 -Wno-unknown-cuda-version"
