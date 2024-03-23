# FROM ubuntu:20.04
FROM telegraf:latest

USER root
RUN apt-get update && \
    apt-get -y install --no-install-recommends \
        apt-utils curl tcpdump mc wget iproute2 openssh-client

# COPY ./etc/install_uf.sh /etc/telegraf/install_uf.sh
# COPY ./etc/user-seed.conf /etc/telegraf/user-seed.conf
# RUN ["chmod", "+x", "/etc/telegraf/install_uf.sh"]
# RUN /bin/bash -c '/etc/telegraf/install_uf.sh'

