#!/usr/bin/python3.6

import sys
import time
import math

MILLNAMES = ['pps', 'kpps', 'mpps', 'gpps']

iface = "eth1" if len(sys.argv) < 2 else sys.argv[1]


def reader(param):
    try:
        stat = '/sys/class/net/{0}/statistics/{1}'.format(iface, param)
        with open(stat) as rx_stat:
            data = rx_stat.read()
        data = float(data) * 8 if param == "rx_bytes" else int(data)
        return data
    except IOError as read_error:
        print(read_error.errno)
        print(read_error)


def humanize_rate(raw_speed):
    n = 2**10
    raw_speed = float(raw_speed) * 8
    if (raw_speed / n**2) >= n:
        return "{0:.2f} Gbits/s".format(raw_speed / (n**3))
    elif (raw_speed / n) >= n:
        return "{0:.2f} Mbits/s".format(raw_speed / (n**2))
    elif (raw_speed / n) >= 1:
        return "{0:.2f} Kbits/s".format(raw_speed / n)
    return "{0:.2f} bits/s".format(raw_speed)


def millify(packets):
    millidx = max(0, min(len(MILLNAMES) - 1, int(math.floor(0 if packets == 0 else math.log10(abs(packets)) / 3))))
    return '{0} {1}'.format(packets / 10**(3 * millidx), MILLNAMES[millidx])


if __name__ == "__main__":
    for i in range(10):
        prev_bites = reader("rx_bytes")
        prev_packets = reader("rx_packets")
        time.sleep(1)
        cur_bites = reader("rx_bytes")
        cur_packets = reader("rx_packets")
        print(humanize_rate(cur_bites - prev_bites), millify(cur_packets - prev_packets))
