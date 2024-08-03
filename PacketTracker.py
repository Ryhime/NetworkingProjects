import pyshark

capture = pyshark.LiveCapture(interface='enp42s0')
capture.sniff(100)

numPackets = 0
ipAddresses = {}
for packet in capture:
    numPackets+=1
    try:
        ip = packet.ip.src
        if (ip not in ipAddresses):
            ipAddresses[ip] = 0
        else:
            ipAddresses[ip] += 1
    except:
        pass

print(ipAddresses)
