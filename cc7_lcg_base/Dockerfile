FROM gitlab-registry.cern.ch/acts/machines/cc7

RUN yum install -y http://linuxsoft.cern.ch/wlcg/centos7/x86_64/wlcg-repo-1.0.0-1.el7.noarch.rpm \
    && yum install -y HEP_OSlibs \
    && yum-config-manager --add-repo https://lcgpackages.web.cern.ch/lcgpackages/rpms/etc/yum.repos.d/lcg.repo \
    && yum clean all
