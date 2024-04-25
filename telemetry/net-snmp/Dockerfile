# Use Ubuntu as the base image
FROM ubuntu:latest

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# Update the package repository
RUN apt-get update

# Install Net-SNMP and Net-SNMP utilities
RUN apt-get install -y snmp snmpd snmp-mibs-downloader

# Copy your SNMP configuration into the container
# Uncomment the following lines and add your snmpd.conf file to the same directory as this Dockerfile
COPY snmp.conf /etc/snmp/snmp.conf
COPY snmpd.conf /etc/snmp/snmpd.conf
COPY /mibs /usr/share/snmp/mibs
# Expose the default SNMP port
EXPOSE 161/udp

# Start the SNMP daemon
CMD ["/usr/sbin/snmpd", "-f"]



# snmpwalk -v3 -u cisco -l authPriv -a MD5 -A cisco123 -x DES -X cisco123 198.18.133.1 1.3.6.1.4.1.9.9.221.1.1.1.1.7
# snmptranslate -Td CISCO-ENHANCED-MEMPOOL-MIB::cempMemPoolTable



