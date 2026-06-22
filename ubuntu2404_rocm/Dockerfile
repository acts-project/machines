# Docker machinery, part of the ACTS project
#
# (c) 2024 CERN for the benefit of the ACTS project
#
# Mozilla Public License Version 2.0

# Start from the (at the time of writing) latest Acts Ubuntu 24.04 image.
# @TODO: Update this
FROM ghcr.io/acts-project/ubuntu2404:82

# Some description for the image.
LABEL description="Ubuntu 24.04 with Acts dependencies and ROCm/HIP"
LABEL maintainer="Stephen Nicholas Swatman <stephen.nicholas.swatman@cern.ch>"
LABEL version="1"
ARG CACHEBUST=0

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
