FROM cern/cc7-base:latest

LABEL description="CERN CentOS 7 with minimal LCG dependencies"
LABEL maintainer="Moritz Kiehn <msmk@cern.ch>"
# increase whenever any of the RUN commands change
LABEL version="4"

# Install all LCG dependencies from the system package manager by using the
# HEP_OSlibs metapackage as described here
#
#     https://gitlab.cern.ch/linuxsupport/rpms/HEP_OSlibs
#
RUN yum -y update \
  && yum -y install HEP_OSlibs \
  && yum -y clean all
