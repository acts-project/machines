FROM ubuntu:20.04

LABEL description="Ubuntu with clang-format v10"
LABEL maintainer="Paul Gessinger <paul.gessinger@cern.ch>"
# increase whenever any of the RUN commands change
LABEL version="1"

RUN apt-get -y update \
  && apt-get -y install clang-format-10 git \
  && apt-get clean all \
  && update-alternatives \
    --install /usr/bin/clang-format clang-format /usr/bin/clang-format-10 100 \
    --slave /usr/bin/clang-format-diff clang-format-diff /usr/bin/clang-format-diff-10 \
    --slave /usr/bin/git-clang-format git-clang-format /usr/bin/git-clang-format-10

