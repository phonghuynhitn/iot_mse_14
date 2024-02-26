import time

print("Xin Chao")
import sys
from Adafruit_IO import MQTTClient
import time
timer_counter = 0
timer_flag = 0

def setTimer(duration):
    global timer_counter, timer_flag
    timer_counter = duration
    timer_flag = 0

def timerRun():
    global timer_counter
    global timer_flag
    if (timer_counter > 0):
        timer_counter -= 1
        if(timer_counter <= 0):
            timer_flag = 1
status = 1
setTimer(2)
while True:
    if status == 1:
        if(timer_flag == 1):
            print("Publish data 1")
            status = 2
            setTimer(5)
        pass
    elif status == 2:
        if(timer_flag == 1):
            print("Publish data 2")
            status = 3
            setTimer(5)
        
        pass
    elif status == 3:
        if (timer_flag == 1):
            print("Publish data 3")
            status = 1
            setTimer(5)
        pass

    timerRun()
    time.sleep(1)