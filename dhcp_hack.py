from scapy.all import *
import socket
import time

#configure
localiface = "enp0s31f6"

target = 1
target_mac = 'EC:41:18:50:08:A1'
target_ip = '192.168.4.75'
server_ip = '192.168.4.1'
hostname='testtesttest'
#configure end

conf.checkIPaddr = False
if target_mac:
    hw = target_mac
else:
    hw=get_if_hwaddr(localiface)

localmac = hw
requestMAC = hw
localmacraw = requestMAC.replace(':','').decode('hex')

ethernet= Ether(dst='ff:ff:ff:ff:ff:ff',src=hw)
ip= IP(src='0.0.0.0', dst='255.255.255.255')
#ip= IP(src='192.168.4.85', dst='255.255.255.255')
udp = UDP(sport=68, dport=67)

if target:
    myxid = 123456
    bootp = BOOTP(chaddr = localmacraw, xid = myxid, flags = 1)
else:
    bootp = BOOTP(chaddr = localmacraw, xid = RandInt(), flags = 1)

dhcp = DHCP(options=[("message-type","discover"),'end'])
pkt =  ethernet / ip / udp / bootp / dhcp
print pkt.display()

if target:
    sendp(pkt, iface=localiface)
    time.sleep(1)
    myip=target_ip
    sip=server_ip
    xid=myxid
else:
    dhcp_offer = srp1(pkt,iface=localiface)
    myip=dhcp_offer[BOOTP].yiaddr
    sip=dhcp_offer[BOOTP].siaddr
    xid=dhcp_offer[BOOTP].xid
    print dhcp_offer.display()

dhcp_request = Ether(dst='ff:ff:ff:ff:ff:ff',src=hw)/IP(src="0.0.0.0",dst="255.255.255.255")/UDP(sport=68,dport=67)/BOOTP(chaddr=[localmacraw],xid=xid)/DHCP(options=[("message-type","request"),("server_id",sip),("requested_addr",myip),("hostname",hostname),"end"])

print dhcp_request.display()
sendp(dhcp_request,verbose=1,iface=localiface)

