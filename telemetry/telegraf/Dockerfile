FROM my-telegraf:1.0.0

USER root
RUN apt-get update && \
    apt-get -y install --no-install-recommends \
        apt-utils curl tcpdump mc wget iproute2 openssh-client \
        snmp snmpd nano make

COPY ./mibs/*.txt /usr/share/snmp/mibs/
COPY ./iana/  /var/lib/mibs/iana
COPY ./ietf/  /var/lib/mibs/ietf
RUN ln -s /var/lib/mibs/iana /usr/share/snmp/mibs/iana
RUN ln -s /var/lib/mibs/ietf /usr/share/snmp/mibs/ietf


# #Makefile for mib-downloader
# #

# CONFFILES= snmp-mibs-downloader.conf \
#            iana.conf ianalist \
#            rfc.conf rfclist rfcmibs.diff \
#            simpleweb.conf simplelist \
#            ianarfc.conf ianarfclist

# BINFILES=  download-mibs
# INSTALL=   /usr/bin/install

# all:

# install:
# 	mkdir /usr/share/doc/mibrfcs
# 	mkdir /usr/share/doc/mibiana
# 	mkdir -p /usr/share/mibs/ietf
# 	mkdir -p /usr/share/mibs/iana
# 	mkdir /etc/snmp-mibs-downloader
# 	$(INSTALL) -m 755 $(BINFILES)  $(DESTDIR)/usr/bin
# 	$(INSTALL) -m 644 $(CONFFILES) $(DESTDIR)/etc/snmp-mibs-downloader
# 	cp mibrfcs/*                   $(DESTDIR)/usr/share/doc/mibrfcs
# 	cp mibiana/*                   $(DESTDIR)/usr/share/doc/mibiana
# 	ln -s /var/lib/mibs/ietf     $(DESTDIR)/usr/share/mibs/ietf
# 	ln -s /var/lib/mibs/iana     $(DESTDIR)/usr/share/mibs/iana


# clean: 
# 	rm -rf /etc/snmp-mibs-downloader
# 	rm -rf /usr/share/doc/mibrfcs
# 	rm -rf /usr/share/doc/mibiana
# 	rm -rf /usr/share/mibs/ietf
# 	rm -rf /usr/share/mibs/iana        


