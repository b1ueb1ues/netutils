from scapy.all import *

localiface = "enp3s0"
hw=get_if_hwaddr("enp3s0")
localmac = hw
hostname='antscam-fjd-kal-jfkl'
requestMAC = hw
localmacraw = requestMAC.replace(':','').decode('hex')

ethernet= Ether(dst='ff:ff:ff:ff:ff:ff',src=hw)
ip= IP(src='0.0.0.0', dst='255.255.255.255')
udp = UDP(sport=68, dport=67)
bootp = BOOTP(chaddr = localmacraw, xid = RandInt(), flags = 1)
dhcp = DHCP(options=[("message-type","discover"),'end'])
pkt =  ethernet / ip / udp / bootp / dhcp
print pkt.display()


#dhcp_offer = srp1(pkt,iface=localiface)
dhcp_offer = sendp(pkt,iface=localiface)


myip=dhcp_offer[BOOTP].yiaddr
sip=dhcp_offer[BOOTP].siaddr
xid=dhcp_offer[BOOTP].xid
dhcp_request = IP(src="0.0.0.0",dst="255.255.255.255")/UDP(sport=68,dport=67)/BOOTP(chaddr=localmacraw,xid=xid)/DHCP(options=[("message-type","request"),("server_id",sip),("requested_addr",myip),("hostname",myhostname),("param_req_list","pad"),"end"])
print dhcp_request.display()


dhcp_ack = srp1(dhcp_request,iface=localiface)
print dhcp_ack.display()







exit()
send(pkt)
