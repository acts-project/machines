# Docker machinery, part of the ACTS project
#
# (c) 2024 CERN for the benefit of the ACTS project
#
# Mozilla Public License Version 2.0

# Start from the (at the time of writing) latest Acts Ubuntu 24.04 image.
FROM ghcr.io/acts-project/ubuntu2404:53

# Some description for the image.
LABEL description="Ubuntu 24.04 with Acts dependencies and oneAPI"
LABEL maintainer="Stephen Nicholas Swatman <stephen.nicholas.swatman@cern.ch>"

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

# Set up the environment. Note that one *MUST* source the
# /opt/intel/oneapi/setvars.sh script to make the following work. Which has to
# be done in the respective CI scripts.
ENV CC="icx"
ENV CXX="icpx"
ENV SYCLCXX="icpx"
ENV SYCLFLAGS="-fsycl -fsycl-targets=spir64,spir64_x86_64"
