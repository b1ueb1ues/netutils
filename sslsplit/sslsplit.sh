#!/bin/bash
iptables -t nat -A PREROUTING -p tcp --dport 443 -j REDIRECT --to-ports 10443
sslsplit -D -P -L https.out -k ca.key -c ca.crt ssl 0.0.0.0 10443 

#>/dev/null 2>&1

#iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-ports 1080
#./sslsplit -D -P -L https.out -k ca.key -c ca.crt ssl 0.0.0.0 10443 tcp 0.0.0.0 10080 
