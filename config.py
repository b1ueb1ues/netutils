from forward import *

class forward():
    interface = 'enp8s0'
    targetip = '192.168.31.85'
    hostip = '192.168.31.1'

    _END = -1

    port_redirect = [
            80,
            443,
            #8053,
            _END
            ]


    ipforward = 1

    twrecycle = 0

    if 0 :
        port_redirect = [
                _END
                ]

    arpspoofr = 1
    arpspoof2 = 0

if __name__ == "__main__" :
    run()
