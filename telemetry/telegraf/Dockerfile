FROM my-telegraf:1.0.0

USER root
RUN apt-get update && \
    apt-get -y install --no-install-recommends \
        apt-utils curl tcpdump mc wget iproute2 openssh-client

