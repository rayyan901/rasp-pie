# Import libraries
import RPi.GPIO as GPIO
import time

#===
switchPos = 5.5
restPos = 7.5
timeout=0.03
#===
# Set GPIO numbering mode
GPIO.setmode(GPIO.BOARD)
#GPIO.cleanup()
# Set pin 8/gpio14 as an output, and set servo1 as pin 8 as PWM
GPIO.setup(11,GPIO.OUT)
servo1 = GPIO.PWM(11,50) # Note 11 is pin, 50 = 50Hz pulse

#start servo=========================
servo1.start(0)
print ('Waiting for 2 seconds')
time.sleep(1)
 
servo1.ChangeDutyCycle(switchPos)  #servo go to switch pos
time.sleep(1)
servo1.ChangeDutyCycle(restPos)  #servo go to rest pos
time.sleep(0.5)
servo1.ChangeDutyCycle(0)
time.sleep(1)
#==============================

#set GPIO Pins
GPIO_TRIGGER = 7 #10 #GPIO15
GPIO_ECHO = 12 #GPIO18
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    mulaTime = time.time()
    StartTime = time.time()
    StopTime = time.time()
    
    stayzero=0
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0 and stayzero<timeout:
        stayzero = StartTime-mulaTime
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    #if TimeElapsed <1:
        
    distance = (TimeElapsed * 34300) / 2
 
    return distance
#===============================================

if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            print ("Measured Distance = %.1f cm" % dist)
            
            if dist <= 13 and dist > 0:
                servo1.ChangeDutyCycle(switchPos)  #servo go to switch pos 
                time.sleep(0.5)
                servo1.ChangeDutyCycle(restPos)  #servo go to rest pos
                time.sleep(0.5)
                servo1.ChangeDutyCycle(0)
                time.sleep(1) 
            time.sleep(1)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
