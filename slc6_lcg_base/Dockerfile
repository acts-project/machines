FROM gitlab-registry.cern.ch/acts/machines/slc6

# RUN yum install -y http://linuxsoft.cern.ch/wlcg/sl6/x86_64/wlcg-repo-1.0.0-1.el6.noarch.rpm \
    # && yum install -y HEP_OSlibs \
RUN yum install -y http://linuxsoft.cern.ch/wlcg/sl6/x86_64/HEP_OSlibs_SL6-1.1.13-1.el6.x86_64.rpm \
    && yum-config-manager --add-repo https://lcgpackages.web.cern.ch/lcgpackages/rpms/etc/yum.repos.d/lcg.repo \
    && yum clean all
