FROM gitlab-registry.cern.ch/acts/machines/cc7

RUN yum install -y http://linuxsoft.cern.ch/wlcg/centos7/x86_64/wlcg-repo-1.0.0-1.el7.noarch.rpm \
    && yum install -y HEP_OSlibs \
    && yum-config-manager --add-repo https://lcgpackages.web.cern.ch/lcgpackages/rpms/etc/yum.repos.d/lcg.repo \
    && yum clean all

ENV LCG_PREFIX=96
ENV PLATFORM=x86_64-centos7-gcc8-opt

RUN yum install -y \
      LCG_${LCG_PREFIX}_ROOT_6.18.00_${PLATFORM//-/_}.noarch \
      LCG_${LCG_PREFIX}_CMake_3.14.3_${PLATFORM//-/_}.noarch \
      LCG_${LCG_PREFIX}_eigen_3.3.7_${PLATFORM//-/_}.noarch \
      LCG_${LCG_PREFIX}_pythia8_243_${PLATFORM//-/_}.noarch \
      LCG_${LCG_PREFIX}_cmaketools_1.8_${PLATFORM//-/_}.noarch \
      LCG_${LCG_PREFIX}_lcgenv_1.3.8_${PLATFORM//-/_}.noarch \
      LCG_${LCG_PREFIX}_DD4hep_01_10_${PLATFORM//-/_}.noarch \
      LCG_${LCG_PREFIX}_Geant4_10.05.p01_${PLATFORM//-/_}.noarch \
    && yum clean all

RUN cd /opt/lcg \
    && git clone https://gitlab.cern.ch/adye/lcgcmake.git \
    && /opt/lcg/lcgcmake/cmake/scripts/create_lcg_view.py \
       -l /opt/lcg \
       -r ${LCG_PREFIX} \
       -p ${PLATFORM} \
       /opt/lcg/views/LCG_${LCG_PREFIX}/${PLATFORM}
