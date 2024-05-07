FROM ghcr.io/acts-project/ubuntu2204

LABEL description="Ubuntu 22.04 with Acts dependencies"
LABEL maintainer="Paul Gessinger <paul.gessinger@cern.ch>"
# increase whenever any of the RUN commands change
LABEL version="1"

# DEBIAN_FRONTEND ensures non-blocking operation (tzdata is a problem)
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update -y \
  && apt-get upgrade -y \
  && apt-get install -y \
  supertuxkart \
  && apt-get clean -y
