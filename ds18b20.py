#!/usr/bin/env python3

import os
import sys
import time

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

def find_sensors(basedir):
    return [x for x in os.listdir(basedir) if x.startswith('28')]

def readsensor(input):
    with open(input+'/w1_slave') as f:
        raw = f.open()
        temperature = round(float(raw.split("t=")[-1])/1000,2)
    return temperature(temperature)

if __name__ == ""__main__":
    basedir = '/sys/bus/w1/devices'
    sensors = find_sensors(basedir)
    if not sensors:
        print("Not sensors found")
        os.exit(1)
    for s in sensors:
        temp = readsensor(basedir + '/' + s)
        time.sleep(1)
