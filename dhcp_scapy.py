from scapy.all import *
import socket

conf.checkIPaddr = False
localiface = "enp0s31f6"
#hw=get_if_hwaddr(localiface)
hw = 'EC:41:18:50:08:A1'

localmac = hw
#myhostname='antscam-fjd-kal-jfkl'
myhostname='test'
requestMAC = hw
localmacraw = requestMAC.replace(':','').decode('hex')

ethernet= Ether(dst='ff:ff:ff:ff:ff:ff',src=hw)
ip= IP(src='0.0.0.0', dst='255.255.255.255')
#ip= IP(src='192.168.4.85', dst='255.255.255.255')
udp = UDP(sport=68, dport=67)

if 0:
    myxid = 123456
    bootp = BOOTP(chaddr = localmacraw, xid = myxid, flags = 1)
else:
    bootp = BOOTP(chaddr = localmacraw, xid = RandInt(), flags = 1)
dhcp = DHCP(options=[("message-type","discover"),'end'])
pkt =  ethernet / ip / udp / bootp / dhcp
print pkt.display()


dhcp_offer = srp1(pkt,iface=localiface)
myip=dhcp_offer[BOOTP].yiaddr
sip=dhcp_offer[BOOTP].siaddr
xid=dhcp_offer[BOOTP].xid
print dhcp_offer.display()

#sendp(pkt,iface=localiface)
#myip = '192.168.4.85'
#sip = '192.168.4.1'
#xid=myxid

#sr = socket.socket()
#sr.bind(('0.0.0.0',68))
#sr.recv(1024)

#dhcp_request = Ether(dst='ff:ff:ff:ff:ff:ff',src=hw)/IP(src="0.0.0.0",dst="255.255.255.255")/UDP(sport=68,dport=67)/BOOTP(chaddr=[localmacraw],xid=xid)/DHCP(options=[("message-type","request"),("server_id",sip),("requested_addr",myip),("hostname",myhostname),("param_req_list","pad"),"end"])
myip = '192.168.4.77'
dhcp_request = Ether(dst='ff:ff:ff:ff:ff:ff',src=hw)/IP(src="0.0.0.0",dst="255.255.255.255")/UDP(sport=68,dport=67)/BOOTP(chaddr=[localmacraw],xid=xid)/DHCP(options=[("message-type","request"),("server_id",sip),("requested_addr",myip),("hostname",myhostname),"end"])

print dhcp_request.display()
sendp(dhcp_request,verbose=1,iface=localiface)

#dhcp_request = IP(src=myip,dst="255.255.255.255")/UDP(sport=68,dport=67)/BOOTP(chaddr=localmacraw,xid=xid)/DHCP(options=[("message-type","request"),("server_id",sip),("requested_addr",myip),("hostname",myhostname),("param_req_list","pad"),"end"])
#print dhcp_request.display()
#send(dhcp_request)

exit()
dhcp_ack = srp1(dhcp_request,iface=localiface)
print dhcp_ack.display()



exit()
send(pkt)
