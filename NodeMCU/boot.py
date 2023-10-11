#Group - Watchmen

#importing libraries
from hcsr04 import HCSR04
from machine import Pin

#stating the pins for the ultrasonic sensor
sensor = HCSR04(trigger_pin=4, echo_pin=5)
#buzzer output pin
buzzer = Pin(14, Pin.OUT)

#loop to constantly check the distance 
while (True):
    #inbuilt function in the hcsr04 library to get the distance
    distance = sensor.distance_cm()
    print('Distance:', distance, 'cm')

    if distance > 0 and distance < 70:
        buzzer.value(1) #output to buzzer if distance less than 70 cm
    
    else:
        buzzer.value(0)