# @TODO: Update this
FROM ghcr.io/acts-project/ubuntu2404:82

LABEL description="Ubuntu 24.04 with dependencies for docs"
LABEL maintainer="Paul Gessiner <paul.gessinger@cern.ch>"
# increase whenever any of the RUN commands change
LABEL version="1"

# DEBIAN_FRONTEND ensures non-blocking operation (tzdata is a problem)
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y graphviz texlive-bibtex-extra libeigen3-dev libboost-dev cmake && \
    apt-get clean -y

