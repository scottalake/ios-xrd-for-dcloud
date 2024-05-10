gnmic sub \
      --username cisco --password cisco123 -a 198.18.133.1:57400 \
      --mode stream \
      --stream-mode sample \
      --sample-interval 3s \
      --path Cisco-IOS-XR-ipv4-bgp-oper:bgp/instances/instance/instance-active/default-vrf/global-process-info \
      --insecure \
      --debug 

gnmic sub \
      --username cisco --password cisco123 -a 198.18.133.2:57400 \
      --mode stream \
      --stream-mode sample \
      --sample-interval 3s \
      --path Cisco-IOS-XR-ipv4-bgp-oper:bgp/instances/instance[instance-name='default']/instance-active \
      --insecure \
      --debug 

gnmic sub \
      --username cisco --password cisco123 -a 198.18.133.1:57400 \
      --mode stream \
      --stream-mode sample \
      --sample-interval 3s \
      --path Cisco-IOS-XR-ipv4-bgp-oper:bgp/instances/instance[instance-name=*]/instance-active \
      --insecure \
      --debug 


gnmic sub \
      --username cisco --password cisco123 -a 198.18.133.1:57400 \
      --mode stream \
      --stream-mode sample \
      --sample-interval 3s \
      --path Cisco-IOS-XR-ipv4-bgp-oper:bgp/instances/instance/instance-active/default-vrf/afs/af/neighbor-af-table/neighbor/update-messages-out \
      --insecure \
      --debug 

gnmic sub \
      --username cisco --password cisco123 -a 198.18.133.1:57400 \
      --mode stream \
      --stream-mode sample \
      --sample-interval 3s \
      --path Cisco-IOS-XR-ipv4-bgp-oper:bgp/instances/instance/instance-active/default-vrf/afs/af/neighbor-af-table/neighbor/update-messages-in \
      --insecure \
      --debug 


gnmic sub \
      --username cisco --password cisco123 -a 198.18.133.1:57400 \
      --mode stream \
      --stream-mode sample \
      --sample-interval 3s \
      --path Cisco-IOS-XR-pfi-im-cmd-oper:interfaces/interface-xr/interface/interface-statistics/full-interface-stats \
      --insecure \
      --debug 

      --username cisco --password cisco123 -a 198.18.133.1:57400 \
      --mode stream \
      --stream-mode sample \
      --sample-interval 3s \
      --path Cisco-IOS-XR-pfi-im-cmd-oper:interfaces/interface-xr/interface/interface-statistics/full-interface-stats \
      --insecure \
      --debug 




♦






#! Testing only
gnmic --username cisco --password cisco123 -a 198.18.133.1:57400 --skip-verify sub --mode stream --stream-mode sample --sample-interval 3s --path Cisco-IOS-XR-ipv4-bgp-oper:bgp/instances/instance/instance-active/default-vrf/neighbors --debug
gnmic --username cisco --password cisco123 -a 198.18.133.1:57400               sub --mode stream --stream-mode sample --sample-interval 3s --path Cisco-IOS-XR-ipv4-bgp-oper:bgp/instances/instance/instance-active/default-vrf/neighbors --debug
gnmic --username cisco --password cisco123 -a 198.18.133.1:57400 --skip-verify sub --mode stream --stream-mode sample --sample-interval 3s --path Cisco-IOS-XR-ipv4-bgp-oper:bgp/instances/instance/instance-active/default-vrf/neighbors --insecure --debug 
gnmic --username cisco --password cisco123 -a 198.18.133.1:57400               sub --mode stream --stream-mode sample --sample-interval 3s --path Cisco-IOS-XR-infra-statsd-oper:infra-statistics/interfaces/interface/latest/generic-counters --debug



#! Working
gnmic --username cisco --password cisco123 -a 198.18.133.1:57400               sub --mode stream --stream-mode sample --sample-interval 3s --path Cisco-IOS-XR-ipv4-bgp-oper:bgp/instances/instance/instance-active/default-vrf/global-process-info --insecure --debug 

gnmic --username cisco --password cisco123 -a 198.18.133.2:57400               sub --mode stream --stream-mode sample --sample-interval 3s --path Cisco-IOS-XR-wdsysmon-fd-oper:system-monitoring/cpu-utilization[node-name=0/RP0/CPU0]/total-cpu-one-minute --insecure --debug 
gnmic --username cisco --password cisco123 -a 198.18.133.6:57400               sub --mode stream --stream-mode sample --sample-interval 3s --path Cisco-IOS-XR-wdsysmon-fd-oper:system-monitoring/cpu-utilization[node-name=0/RP0/CPU0]/total-cpu-one-minute --insecure --debug 

root@2f534a5a7844:/# snmpwalk -v3 -u cisco -l authPriv -a MD5 -A cisco123 -x DES -X cisco123 198.18.133.5 1.3.6.1.2.1.47.1.1.1.1.7
iso.3.6.1.2.1.47.1.1.1.1.7.1 = STRING: "0/RP0"
iso.3.6.1.2.1.47.1.1.1.1.7.2 = STRING: "0/RP0-Virtual-Motherboard"
iso.3.6.1.2.1.47.1.1.1.1.7.3 = STRING: "0/RP0-Virtual-IDPROM"
iso.3.6.1.2.1.47.1.1.1.1.7.4 = STRING: "0/RP0-MgmtEth0/RP0/CPU0/0"
iso.3.6.1.2.1.47.1.1.1.1.7.10 = STRING: "0/RP0-CPU Module"
iso.3.6.1.2.1.47.1.1.1.1.7.11 = STRING: "0/RP0-Intel 8 Core CPU Complex"
iso.3.6.1.2.1.47.1.1.1.1.7.12 = STRING: "0/RP0-Virtual processor for sysadmin"
iso.3.6.1.2.1.47.1.1.1.1.7.13 = STRING: "0/RP0-Virtual processor for RP IOS-XR"
iso.3.6.1.2.1.47.1.1.1.1.7.14 = STRING: "0/RP0-Virtual processor for LCP XR"
iso.3.6.1.2.1.47.1.1.1.1.7.65537 = STRING: "0/0"
iso.3.6.1.2.1.47.1.1.1.1.7.65538 = STRING: "0/0-Virtual-Motherboard"
iso.3.6.1.2.1.47.1.1.1.1.7.65539 = STRING: "0/0-Virtual-IDPROM"
iso.3.6.1.2.1.47.1.1.1.1.7.65546 = STRING: "0/0-Ether Port container 0"

iso.3.6.1.2.1.47.1.1.1.1.7.10 = STRING: "0/RP0-CPU Module"
snmpwalk -v3 -u cisco -l authPriv -a MD5 -A cisco123 -x DES -X cisco123 198.18.133.5 iso.3.6.1.2.1.47.1.1.1.1.7.10


Xpath	/
Prefix	wdsysmon-fd-oper



gnmic -a 198.18.133.1:57400 -u cisco -p cisco123 --insecure capabilities 

  #   origin = "Cisco-IOS-XR-infra-statsd-oper"
  #   path = "infra-statistics/interfaces/interface/latest/generic-counters"















#Cisco-IOS-XR-ipv4-bgp-oper:bgp/instances/instance[instance-name='default']/instance-active

#gnmic --username cisco --password cisco123 -a 198.18.133.1:57400 --skip-verify sub --stream-mode sample --sample-interval 3s --path  Cisco-IOS-XR-ipv4-bgp-oper:bgp/instances/instance/instance-active/default-vrf/global-process-info

#gnmic --username cisco --password cisco123 -a 198.18.133.6:57400 --skip-verify sub --stream-mode sample --sample-interval 3s --path  Cisco-IOS-XR-ipv4-bgp-oper:bgp/instances/instance[instance-name='default']/instance-active
#gnmic --username cisco --password cisco123 -a 198.18.133.6:57400 --skip-verify sub --stream-mode sample --sample-interval 3s --path  Cisco-IOS-XR-ipv4-bgp-oper:bgp/instances/instance[instance-name=*]/instance-active
#gnmic --username cisco --password cisco123 -a 198.18.133.6:57400 --skip-verify sub --stream-mode sample --sample-interval 3s --path  Cisco-IOS-XR-ipv4-bgp-oper:bgp/instances/instance/instance-active

# gnmic subscribe --username cisco --password cisco123 -a 198.18.133.6:57400 \
#       --skip-verify \
#       --sample-interval 3s \
#       --mode stream \
#       --stream-mode sample \
#       --path  Cisco-IOS-XR-ipv4-bgp-oper:bgp/instances/instance[instance-name='default']/instance-active


# # gnmic -a 192.0.2.1:6030 -u admin -p admin --insecure capabilities  \
# #   >> outputs/capabilities.json

# gnmic -a 198.18.133.5:57400 -u cisco -p cisco123 --insecure capabilities  \
#   >> ./capabilities.json



#gnmic --username admin --password C1sco12345 -a 198.18.133.101:57400 --skip-verify sub --mode stream --stream-mode sample --sample-interval 3s --path  Cisco-IOS-XR-ipv4-bgp-oper:bgp/instances/instance/instance-active/default-vrf/global-process-info

#gnmic --username admin --password C1sco12345 -a 198.18.133.101:57400 --skip-verify sub --mode stream --stream-mode sample --sample-interval 3s --path  Cisco-IOS-XR-ipv4-bgp-oper:bgp/instances/instance[instance-name='default']/instance-active
#gnmic --username admin --password C1sco12345 -a 198.18.133.101:57400 --skip-verify sub --mode stream --stream-mode sample --sample-interval 3s --path  Cisco-IOS-XR-ipv4-bgp-oper:bgp/instances/instance[instance-name=*]/instance-active
#gnmic --username admin --password C1sco12345 -a 198.18.133.101:57400 --skip-verify sub --mode stream --stream-mode sample --sample-interval 3s --path  Cisco-IOS-XR-ipv4-bgp-oper:bgp/instances/instance/instance-active

#gnmic -a 198.18.133.1:57400 -u cisco -p cisco123 --insecure capabilities



# gnmic -a 198.18.133.101:57400 --username admin --password C1sco12345 --insecure subscribe \
#   --path "Cisco-IOS-XR-ipv4-bgp-oper/bgp/instances/instance[instance-name='default']/instance-active" \
#   --mode stream --stream-mode sample




# gnmic --username cisco --password cisco123 -a 198.18.133.1:57400 --skip-verify sub --stream-mode sample \ 
#   --sample-interval 3s --path  Cisco-IOS-XR-wdsysmon-fd-oper:system-monitoring/cpu-utilization

# gnmic --username cisco --password cisco123 -a 198.18.133.1:57400 --skip-verify sub --stream-mode sample --sample-interval 3s --path  Cisco-IOS-XR-ipv4-bgp-oper:bgp/instances/instance[instance-name='default']/instance-active

#   --path "Cisco-IOS-XR-ipv4-bgp-oper:bgp/instances/instance[instance-name='default']/instance-active" \



# gnmic -a 198.18.133.1:57400 -u cisco -p cisco123 --insecure subscribe \
#   --path "Cisco-IOS-XR-infra-statsd-oper:infra-statistics/interfaces/interface[name='GigabitEthernet0/0/0/1']/latest/generic-counters" \
#   --mode stream --stream-mode sample --sample-interval 1s prompt







# gnmic -a 198.18.133.1:57400 -u cisco -p cisco123 --insecure subscribe --timeout 1m --encoding JSON_IETF \
#   --path "rfc7951:/Cisco-IOS-XR-infra-statsd-oper/infra-statistics/interfaces/interface[interface-name='GigabitEthernet0/0/0/1']/latest/generic-counters" \
#   --mode stream --stream-mode sample


# gnmic -a 198.18.133.1:57400 -u cisco -p cisco123 --insecure subscribe --timeout 1m --encoding JSON_IETF \
#   --path "rfc7951:/Cisco-IOS-XR-infra-statsd-oper/infra-statistics/interfaces/interface[interface-name='GigabitEthernet0/0/0/1']/latest/generic-counters" \
#   --mode stream --stream-mode sample

# gnmic -a 198.18.133.1:57400 -u cisco -p cisco123 --insecure subscribe --timeout 1m --encoding JSON_IETF \
#   --path "rfc7951:Cisco-IOS-XR-infra-statsd-oper:infra-statistics/interfaces/interface[interface-name='GigabitEthernet0/0/0/1']/latest/generic-counters" \
#   --mode stream --stream-mode sample

# gnmic -a 198.18.133.1:57400 -u cisco -p cisco123 --insecure get --timeout 1m --encoding JSON_IETF \
#   --path "rfc7951:Cisco-IOS-XR-infra-statsd-oper:infra-statistics/interfaces/interface[interface-name='GigabitEthernet0/0/0/1']/latest/generic-counters"

#gnmic -a 10.88.171.241:50052 -u admin -p 'Cxlabs!123' --insecure get --path "rfc7951:/Cisco-IOS-XE-bgp-oper:bgp-state-data/bgp-state-data"


# gnmic -a 198.18.133.1:57400 -u cisco -p cisco123 --insecure subscribe --timeout 1m --encoding JSON_IETF \
#   --path "Cisco-IOS-XR-ipv4-bgp-oper:bgp/instances/instance[instance-name='default']/instance-active" \
#   --mode stream --stream-mode sample


# gnmic -a 198.18.133.1:57400 -u cisco -p cisco123 --insecure get --timeout 1m --encoding JSON_IETF \
#   --path "Cisco-IOS-XR-ipv4-bgp-oper:bgp/instances/instance[instance-name='default']/" 



# gnmic -a 198.18.133.1:57400 -u cisco -p cisco123 --insecure subscribe \
#   --path "Cisco-IOS-XR-ipv4-bgp-oper/bgp/instances/instance[instance-name='default']/instance-active" \
#   --mode stream --stream-mode sample


# gnmic -a 198.18.133.1:57400 -u cisco -p cisco123 --insecure subscribe \
#   --path "/bgp/instances/instance[instance-name='default']/instance-active" \
#   --mode stream --stream-mode sample

# /gnmic --address 198.18.133.1:57400 --insecure -e json_ietf \
#         --username cisco --password cisco123 \
#         --file Cisco-IOS-XR-ipv4-bgp-oper.yang \
#         --dir /home/dcloud \
#         --exclude ietf-interfaces \
#         prompt

# gnmic -a 172.29.11.20:57733 -u admin -p password --insecure --timeout 1m --encoding JSON_IETF get --path 'openconfig-platform:components/component[name='0/0-OpticalChannel0/0/0/8']'


  # [[inputs.gnmi.subscription]]
  #   name = "memory-summary/nodes/node/summary"
  #   origin = "Cisco-IOS-XR-nto-misc-oper"
  #   path = "memory-summary/nodes/node/summary"
  #   subscription_mode = "sample"
  #   sample_interval = "10s"

# gnmic -a 198.18.133.1:57400 -u cisco -p cisco123 --insecure subscribe \
#   --path "Cisco-IOS-XR-ipv4-bgp-oper:bgp/instances/instance/" \
#   --mode stream --stream-mode sample

# gnmic -a 198.18.133.1:57400 -u cisco -p cisco123 --insecure subscribe \
#   --path "rfc7951:/Cisco-IOS-XR-ipv4-bgp-oper:bgp/instances/instance/" \
#   --mode stream --stream-mode sample

# gnmic -a 198.18.133.1:57400 -u cisco -p cisco123 --insecure subscribe \
#   --path "rfc7951:/Cisco-IOS-XR-nto-misc-oper:memory-summary/nodes/node/summary" \
#   --mode stream --stream-mode sample
# gnmic -a 198.18.133.1:57400 -u cisco -p cisco123 --insecure subscribe \
#   --path "/Cisco-IOS-XR-nto-misc-oper:memory-summary/nodes/node/summary" \
#   --mode stream --stream-mode sample

# gnmic -a 10.88.171.241:50052 -u admin -p 'Cxlabs!123' --insecure get --path "rfc7951:/Cisco-IOS-XE-interfaces-oper:interfaces/interface[name=TwentyFiveGigE1/1/2]/name"



# Name	instance
# Nodetype	list
# Description	Instance specific BGP data
# Module	Cisco-IOS-XR-ipv4-bgp-oper
# Revision	2023-02-03
# Xpath	/bgp/instances/instance
# Prefix	ipv4-bgp-oper
# Namespace	http://cisco.com/ns/yang/Cisco-IOS-XR-ipv4-bgp-oper
# Schema Node Id	/bgp/instances/instance
# Keys	
# "instance-name"
# Access	read-only
# Operations	
# "get"


