FROM cern/c8-base:latest

LABEL description="CERN CentOS 8"
LABEL maintainer="Paul Gessinger <paul.gessinger@cern.ch>"
LABEL version="1"

RUN dnf install -y https://linuxsoft.cern.ch/wlcg/centos8/x86_64/HEP_OSlibs-8.2.0-2.el8.x86_64.rpm \
  && dnf -y clean all
