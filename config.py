def getips():
    import subprocess
    lip = subprocess.check_output("hostname -I",shell=1).strip('\n')
    tmprip = subprocess.check_output("ip route |grep default|awk '{print $3}'",shell=1)
    rip = str(tmprip).strip('\n')
    return lip,rip

class netutils_config():
    interface = 'enp0s31f6'
    targetip = '192.168.28.193'
    #hostip = '192.168.28.1'
    myip, hostip = getips()
    ipforward = 1
    arpspoofr = 1
    port_redirect = 0

    arpspoof2 = 0
    twrecycle = 0

    _END = -1


    if port_redirect :
        port_redirect = [
                80,
                443,
                #8053,
                _END
                ]
    else:
        port_redirect = [
                _END
                ]


if __name__ == "__main__" :
    import netutils
    netutils.run()
