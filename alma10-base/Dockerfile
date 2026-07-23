FROM gitlab-registry.cern.ch/linuxsupport/alma10-base:latest

LABEL description="CERN AlmaLinux 10"
LABEL maintainer="Paul Gessinger <paul.gessinger@cern.ch>"
LABEL version="1"
ARG CACHEBUST=0

RUN dnf install -y epel-release \
  && dnf install -y https://linuxsoft.cern.ch/wlcg/el10/x86_64/HEP_OSlibs-10.0.4-2.el10.x86_64.rpm \
  && dnf install -y unzip gcc-toolset-15 ninja-build expat-devel \
  && dnf -y clean all

ENV CXX=/opt/rh/gcc-toolset-15/root/usr/bin/g++
ENV CC=/opt/rh/gcc-toolset-15/root/usr/bin/gcc
