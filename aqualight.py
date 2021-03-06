#!/usr/bin/python3
import pigpio
import math
import yaml
import datetime
import time

pi = pigpio.pi()

data = yaml.load(open('day.yaml'))
#print(yaml.dump(data))

def flat(value):
    #print("flat at %d" % value)
    return value

def ramp_up(minute, minutes):
    rad = minute * math.pi / minutes
    mycos = (1 - math.cos(rad))/2
    #print("%f %f" % (rad, mycos))
    return mycos

def ramp_down(minute, minutes):
    rad = (minutes - minute) * math.pi / minutes
    mycos = (1 - math.cos(rad))/2
    #print("%f %f" % (rad, mycos))
    return mycos

def get_level(now, colour):
    now_hm = datetime.time(now.hour, now.minute, now.second)
    now_minutes = 60 * now.hour + now.minute
    print("now %s" % now_hm)
    for color, time_slots in data.items():
        #print(color) 
        if color == colour:
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
                        level = flat(slot_value)
                        #print("Flat at %d" % slot_value)
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

def main():
    oldlevel = 0
    while 1:
        now = datetime.datetime.now()
        newlevel = get_level(now, 'white')
        if newlevel != oldlevel:
            print("Set new level %f" % newlevel)
            oldlevel = newlevel
            pi.hardware_PWM(18, 1000, int(newlevel*1e6))
        else:
            print("Keep old level %f" % oldlevel)
        time.sleep(60)

def testrun():
    # test run an entire day
    just1minute = datetime.timedelta(minutes=1)
    now = datetime.datetime.now()
    for i in range(0, 60*24, 15):
        fakenow = now + i * just1minute
        level = get_level(fakenow, 'white')
        print(level)
        pi.hardware_PWM(18, 1000, int(level*1e6))
        time.sleep(1)

if __name__ == "__main__":
    main()

