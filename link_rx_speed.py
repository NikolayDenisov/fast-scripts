#!/usr/bin/env python

import sys
import time


def getbites():
    iface = "eth1" if len(sys.argv) < 2 else sys.argv[1]
    with open('/sys/class/net/{0}/statistics/rx_bytes'.format(iface)) as rx:
        rx_bytes = rx.read()
    return float(rx_bytes) * 8


def humanize_rate(raw_speed):
    n = 2**10
    if (raw_speed / n**2) >= n**2:
        return "{0:.2f} Gbits/s".format(raw_speed / (n**3))
    elif (raw_speed / n) >= n:
        return "{0:.2f} Mbits/s".format(raw_speed / (n**2))
    elif (raw_speed / n) >= 1:
        return "{0:.2f} Kbits/s".format(raw_speed / n)
    return "{0:.2f} bits/s".format(raw_speed)

if __name__ == "__main__":
    for i in range(10):
        prev = getbites()
        time.sleep(1)
        cur = getbites()
        print humanize_rate(cur - prev)
