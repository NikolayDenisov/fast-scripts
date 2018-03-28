#!/usr/bin/env python

import math
import os
import subprocess

chars = "MGT%"
os.environ['LANG'] = ''
command = "df -Ph --block-size=M| tail -n +2 | awk '{print $2, $5}'"
process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
(out, err) = process.communicate()
table = out.strip().split('\n')
for line in table:
    total, percent = line.translate(None, chars).split(' ')
    total = float(total)
    percent = int(percent)
    if (total >= 2 ** 10) and (total < 2 ** 20):
        total = total / 1000.0
    elif total >= 2 ** 20:
        total = total / 10000.0
    used = (total * (percent / 100))
    free = total - used
    limit = math.sqrt(total)
    print(free, limit)
    if free < limit:
        exit(1)
