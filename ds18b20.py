#!/usr/bin/python3

import os
import sys
import time

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')


def find_sensors(basedir):
    return [x for x in os.listdir(basedir) if x.startswith('28')]


def readsensor(data):
    with open(data + '/w1_slave') as f:
        raw = f.open()
        temperature = round(float(raw.split("t=")[-1]) / 1000, 2)
    return temperature(temperature)


if __name__ == "__main__":
    basedir = '/sys/bus/w1/devices'
    SENSORS = find_sensors(basedir)
    if not SENSORS:
        print("Not sensors found")
        sys.exit(1)
    for s in SENSORS:
        temp = readsensor(basedir + '/' + s)
        time.sleep(1)
