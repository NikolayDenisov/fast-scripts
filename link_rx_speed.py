#!/usr/bin/env python

import sys
import time

iface = "eth1" if len(sys.argv) < 2 else sys.argv[1]

def getbites():
    try:
        with open('/sys/class/net/{0}/statistics/rx_bytes'.format(iface)) as rx:
            rx_bytes = rx.read()
        return float(rx_bytes) * 8
    except IOError as e:
        print e.errno
        print e

def getpackets():
    try:
        with open('/sys/class/net/{0}/statistics/rx_packets'.format(iface)) as rx:
            rx_packets = rx.read()
        return int(rx_packets)
    except IOError as e:
        print e.errno
        print e
    
def humanize_rate(raw_speed):
    n = 2**10
    if (raw_speed / n**2) >= n:
        return "{0:.2f} Gbits/s".format(raw_speed / (n**3))
    elif (raw_speed / n) >= n:
        return "{0:.2f} Mbits/s".format(raw_speed / (n**2))
    elif (raw_speed / n) >= 1:
        return "{0:.2f} Kbits/s".format(raw_speed / n)
    return "{0:.2f} bits/s".format(raw_speed)

if __name__ == "__main__":
    for i in range(10):
        prev_bites = getbites()
        prev_packest = getpackets() 
        time.sleep(1)
        cur_bites  = getbites()
        cur_packest  = getpackets()
        print humanize_rate(cur_bites - prev_bites), (cur_packest - prev_packest), "pkts/s"
