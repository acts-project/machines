# Docker machinery, part of the ACTS project
#
# (c) 2024 CERN for the benefit of the ACTS project
#
# Mozilla Public License Version 2.0

FROM ubuntu:24.04

LABEL description="Ubuntu with clang-format v18"
LABEL maintainer="Stephen Nicholas Swatman <stephen.nicholas.swatman@cern.ch>"
# increase whenever any of the RUN commands change
LABEL version="1"

RUN apt-get -y update \
  && apt-get -y install clang-format-18 git \
  && apt-get clean all \
  && update-alternatives \
    --install /usr/bin/clang-format clang-format /usr/bin/clang-format-18 100 \
    --slave /usr/bin/clang-format-diff clang-format-diff /usr/bin/clang-format-diff-18 \
    --slave /usr/bin/git-clang-format git-clang-format /usr/bin/git-clang-format-18
