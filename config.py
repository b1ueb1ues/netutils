def getips():
    import subprocess
    lip = subprocess.check_output("hostname -I",shell=1)
    lip = lip.decode().strip('\\n').strip('\n')
    lip = lip.split(' ')[0]
    
    rip = subprocess.check_output("ip route |grep default|awk '{print $3}'",shell=1)
    rip = rip.decode().strip('\\n').strip('\n')
    return lip,rip

def getmac(ip):
    mac = subprocess.check_output( "arp %s|grep ether|awk '{print $3}'"%ip, shell=1) \
            .decode() \
            .strip('\n')
    if not mac:
        print('no arp for %s'%ip)
        raise
    return mac

def mymac(iface):
    mymac = subprocess.check_output( \
            "ifconfig %s|grep ether|awk '{print $2}'"%iface, shell=1) \
            .decode().strip('\n')
    if not mymac :
        print('no mymac')
        raise
    return mymac



class netutils_config():
    interface = 'enp0s31f6'
    targetip = '192.168.3.90'
    ipforward = 1
    arpspoofr = 1
    port_redirect = 0

    arpspoof2 = 0
    twrecycle = 0

    myip, routerip = getips()
    hostip = routerip
    #hostip = '192.168.4.178'


    if port_redirect :
        port_redirect = {
                80:1080,
                443:10443,
                }
    else:
        port_redirect = {
                }


if __name__ == "__main__" :
    import netutils
    netutils.run()

