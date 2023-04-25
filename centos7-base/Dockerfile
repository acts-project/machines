FROM cern/cc7-base:latest

LABEL description="CERN CentOS 7"
LABEL maintainer="Paul Gessinger <paul.gessinger@cern.ch>"
LABEL version="1"

RUN yum -y install https://linuxsoft.cern.ch/wlcg/centos7/x86_64/HEP_OSlibs-7.3.5-2.el7.cern.x86_64.rpm \
  && yum -y clean all
