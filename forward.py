import mitm

def send(pkt):
    c = pkt.payload.payload
    if c.name == "TCP":
        if tcp.dport == 10443:
            pass


a = mitm.Mitm()
a.send = send
a.run()

