#!/usr/bin/python2
"""script for analyze traffic on ifaces."""

import sys
import os
import time
import math
import subprocess
import copy

MILLNAMES = ['pps', 'kpps', 'mpps', 'gpps']


def reader(param, iface):
    """Read statistics for iface."""
    try:
        stat = '/sys/class/net/{0}/statistics/{1}'.format(iface, param)
        with open(stat) as rx_stat:
            data = rx_stat.read()
        data = float(data) * 8 if param == "rx_bytes" else int(data)
        return data
    except IOError as read_error:
        print(read_error)
        sys.exit(read_error.errno)


def humanize_rate(raw_speed):
    """Convert for human format speed."""
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
    """Convert for human format packets."""
    millidx = max(0, min(len(MILLNAMES) - 1,
                         int(math.floor(0 if packets == 0
                                        else math.log10(abs(packets)) / 3))))
    return '{0} {1}'.format(packets / 10**(3 * millidx), MILLNAMES[millidx])


def get_up_interfaces():
    """Return all up interfaces."""
    cmd = "ip -o link show | grep 'UP' | awk -F': ' '{print $2}' | egrep '(eth|em|en|enp|bond|p[1-9]p)[0-9\.]+' | cut -d '@' -f 1"
    process = subprocess.Popen(
        [cmd], shell=True, stdout=subprocess.PIPE).communicate()[0]
    return [i for i in process.split('\n') if i is not '']


def analyze():
    """Calculate diff for current nad preview data."""
    prev = []
    cur = []
    result = []
    total = []
    for device in get_up_interfaces():
        prev.append((device, reader("rx_bytes", device),
                     reader("rx_packets", device)))
    time.sleep(1)
    os.system('clear')
    for device in get_up_interfaces():
        cur.append((device, reader("rx_bytes", device),
                    reader("rx_packets", device)))
    for i in range(len(cur)):
        result.append([cur[i][0], cur[i][-2] - prev[i]
                       [-2], cur[i][-1] - prev[i][-1]])
    total = copy.deepcopy(result)
    for i in range(len(total)):
        total[i].pop(0)
    total = [sum(x) for x in zip(*total)]
    return result, total


def preview():
    """Humanfriendly output."""
    raw, total = analyze()
    for i in raw:
        print i[0], humanize_rate(i[1]), millify(i[2])
    print
    print 'Total {0} {1}'.format(humanize_rate(total[0]), millify(total[1]))


def get_for_iface(iface):
    """Get statistics about network interface."""
    prev_bites = reader("rx_bytes", iface)
    prev_packets = reader("rx_packets", iface)
    time.sleep(1)
    os.system('clear')
    cur_bites = reader("rx_bytes", iface)
    cur_packets = reader("rx_packets", iface)
    return ' '.join([iface, humanize_rate(cur_bites - prev_bites), millify(cur_packets - prev_packets)])


if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            for i in range(10):
                print get_for_iface("eth1")
        elif sys.argv[1] in '--all':
            for i in range(10):
                preview()
        else:
            iface = sys.argv[1]
            for i in range(10):
                print get_for_iface(iface)
    except KeyboardInterrupt as kill:
        sys.exit(0)
