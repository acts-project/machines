FROM ubuntu:19.10

LABEL description="Ubuntu with clang-format v8"
LABEL maintainer="Moritz Kiehn <msmk@cern.ch>"
# increase whenever any of the RUN commands change
LABEL version="1"

RUN apt-get -y update \
  && apt-get -y install clang-format-8 git \
  && apt-get clean all \
  && update-alternatives \
    --install /usr/bin/clang-format clang-format /usr/bin/clang-format-8 100 \
    --slave /usr/bin/clang-format-diff clang-format-diff /usr/bin/clang-format-diff-8 \
    --slave /usr/bin/git-clang-format git-clang-format /usr/bin/git-clang-format-8

