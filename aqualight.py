#!/usr/bin/python3
import math

#print "sin(math.pi) : ",  math.sin(math.pi)
#print "sin(math.pi/2) : ",  math.sin(math.pi/2)

#maxrange=10
#range_to_rad = math.pi / maxrange;
#range_to_rad_ramp = math.pi / 2 / maxrange;
#print maxrange, range_to_rad, range_to_rad_ramp

#for i in range(maxrange + 1):
#    rad = i * range_to_rad_ramp
#    print "%d %f %f" % (i, rad, math.sin(rad))

#def ramp_up(steps):
#    for i in range(steps+1):
#        rad = i * range_to_rad_ramp
#        print "%d %f %f" % (i, rad, math.sin(rad))
#
#def ramp_down(steps):
#    for i in range(steps+1):
#        rad = (steps - i) * range_to_rad_ramp
#        print "%d %f %f" % (i, rad, math.sin(rad))
#
#ramp_up(10)
#ramp_down(10)

#def ramp_up(steps):
#    for i in range(steps+1):
#        rad = i * math.pi / steps
#        mycos = (1 - math.cos(rad))/2
#        print("%d %f %f" % (i, rad, mycos))
##        p.ChangeDutyCycle(50 * mycos)
##        time.sleep(0.01)
#
#def ramp_down(steps):
#    for i in range(steps+1):
#        rad = (steps - i) * math.pi / steps
#        mycos = (1 - math.cos(rad))/2
#        print("%d %f %f" % (i, rad, mycos))
##        p.ChangeDutyCycle(50 * mycos)
##        time.sleep(0.01)
#
##while 1:
#print("ramp up")
#ramp_up(10)
#print("max")
#
#print("ramp down")
#ramp_down(10)
#print("min")

#from numpy import genfromtxt
#csv = genfromtxt('day.csv', delimiter=',')
#00:00,flat,0
#07:30,ramp-up,3:00,0,1
#10:30,flat,1
#17:00,ramp-down,4:00,1,0.01
#21:00,flat,0.01
#23:00,flat,0
#import numpy as np
#from io import StringIO
##np.genfromtxt(StringIO('day.csv'), comments="#", delimiter=",", autostrip=True)
#csv = np.genfromtxt(StringIO(open('day.csv').read()), comments="#", delimiter=",", autostrip=True, missing_values="", usecols=(0,1,2,3,4))
##print(vars(csv))
#from inspect import getmembers
#from pprint import pprint
##pprint(getmembers(csv))
#pprint(csv)

import yaml
import datetime
import time
import os

data = yaml.load(open('day.yaml'))
#print(yaml.dump(data))

def flat(value):
    #print("flat at %d" % value)
    return value

def ramp_up(minute, minutes):
    rad = minute * math.pi / minutes
    mycos = (1 - math.cos(rad))/2
    #print("%f %f" % (rad, mycos))
#   p.ChangeDutyCycle(50 * mycos)
#   time.sleep(0.01)
    return mycos

def ramp_down(minute, minutes):
    rad = (minutes - minute) * math.pi / minutes
    mycos = (1 - math.cos(rad))/2
    #print("%f %f" % (rad, mycos))
#   p.ChangeDutyCycle(50 * mycos)
#   time.sleep(0.01)
    return mycos

def get_level(now, colour):
    now_hm = datetime.time(now.hour, now.minute, now.second)
    now_minutes = 60 * now.hour + now.minute
    print("now %s" % now_hm)
    for color, time_slots in data.items():
        #print(color) 
        if color == 'white':
            num_time_slots = len(time_slots)
            #print(num_time_slots)
            for index, time_slot in enumerate(time_slots):
                #print(index)
                #print(time_slots[index+1]['start_time'])
                if index+1 == num_time_slots:
                    next_index = 0
                else:
                    next_index = index+1
                start_time = time_slots[next_index]['start_time']
                hour,minute = (int(x) for x in list(map(int, start_time.split(":"))))
                t1 = datetime.time(hour,minute)
                if now_hm < t1 or next_index == 0 :
                    #print("Found in slot %d" % index)
                    slot_type = time_slots[index]['type']
                    start_time = time_slots[index]['start_time']
                    hour,minute = (int(x) for x in list(map(int, start_time.split(":"))))
                    t1_minutes = 60 * hour + minute
                    end_time = time_slots[next_index]['start_time']
                    hour,minute = (int(x) for x in list(map(int, end_time.split(":"))))
                    t2_minutes = 60 * hour + minute
                    delta_t = t2_minutes - t1_minutes
                    if slot_type == 'flat': 
                        slot_value = time_slots[index]['value']
                        #print("Flat at %d" % slot_value)
                        level = flat(slot_value)
                    if slot_type == 'ramp-up':
                        begin_value = time_slots[index]['begin_value']
                        end_value = time_slots[index]['end_value']
                        level = begin_value + (end_value - begin_value) * ramp_up(now_minutes - t1_minutes, delta_t)
                        #print("Ramp up from %s at %d to %s at %d" % (start_time, begin_value, end_time, end_value))
                    if slot_type == 'ramp-down':
                        begin_value = time_slots[index]['begin_value']
                        end_value = time_slots[index]['end_value']
                        level = end_value + (begin_value - end_value) * ramp_down(now_minutes - t1_minutes, delta_t)
                        #print("Ramp down from %s at %d to %s at %d" % (start_time, begin_value, end_time, end_value))
                    break
            return level

#start_time = "07:30"
#end_time   = "10:30"

#hour,minute = (int(x) for x in list(map(int, start_time.split(":"))))
#t1_minutes = 60 * hour + minute
#
#hour,minute = (int(x) for x in list(map(int, end_time.split(":"))))
#t2_minutes = 60 * hour + minute
#
#delta_t = t2_minutes - t1_minutes
#print(delta_t)
#print(now_minutes - t1_minutes)
#level = ramp_up(now_minutes - t1_minutes, delta_t)
#level = ramp_down(now_minutes - t1_minutes, delta_t)

while 1:
    now = datetime.datetime.now()
    level = get_level(now, 'white')
    print(level)
    time.sleep(60)

#now_hm = datetime.time(now.hour, now.minute, now.second)
#now_minutes = 60 * now.hour + now.minute
#print("now %s" % now_hm)

just1minute = datetime.timedelta(minutes=1)
now = datetime.datetime.now()
for i in range(0, 60*24, 15):
    fakenow = now + i * just1minute
    level = get_level(fakenow, 'white')
    print(level)

