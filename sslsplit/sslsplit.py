import subprocess
import os


def run(args,port80=10080,port443=10443):
    cmd = 'sslsplit'
    #cmd += ' -k tools/sslsplit/ca.key -c tools/sslsplit/ca.crt '
    cmd += ' -k ca.key -c ca.crt '
    cmd += ' ssl 0.0.0.0 ' + str(port443)
    cmd += ' tcp 0.0.0.0 ' + str(port80)
    cmd += ' ' + args
    print cmd
    subprocess.Popen(cmd,shell=1)

def stop():
    cmd = "kill `ps aux | grep -m1 'sslsplit -k' | awk '{print $2}'`"
    os.system(cmd)


if __name__ == '__main__' :
    run('-D')
