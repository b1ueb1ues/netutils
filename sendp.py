
from scapy.all import *

def main():
    p = Ether()/IP(src='127.0.0.1',dst='192.168.4.178')/TCP(dport=54355)
    print repr(p)
    a = srp(p)
    print a
   

if __name__ == "__main__" :
    main()
