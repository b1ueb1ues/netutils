#!/bin/bash
#sslsplit -D -P -L https.out -k ca.key -c ca.crt ssl 0.0.0.0 10443 tcp 0.0.0.0 10080 
sslsplit -D -P -L https.out -k ca.key -c ca.crt ssl 0.0.0.0 10443 
#>/dev/null 2>&1
