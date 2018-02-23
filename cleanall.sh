#!/bin/bash
echo '0' > /proc/sys/net/ipv4/tcp_fin_timeout
echo '0' > /proc/sys/net/ipv4/ip_forward
echo '0' > /proc/sys/net/ipv4/tcp_tw_recycle
iptables -t nat -F 
pkill arpspoof
pkill sslsplit
pkill create_ap
#kill `ps aux | grep  arpspoof | awk '{print $2}'`
#kill `ps aux | grep  sslsplit | awk '{print $2}'`
create_ap --stop `create_ap --list-running |grep "[0-9]"|awk '{print $1}'`


