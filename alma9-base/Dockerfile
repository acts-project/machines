FROM cern/alma9-base:latest

LABEL description="CERN AlmaLinux 9"
LABEL maintainer="Paul Gessinger <paul.gessinger@cern.ch>"
LABEL version="1"

RUN dnf install -y https://linuxsoft.cern.ch/wlcg/el9/x86_64/HEP_OSlibs-9.1.0-2.el9.x86_64.rpm \
  && dnf install -y unzip gcc-toolset-14 \
  && dnf -y clean all
