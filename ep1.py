import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

led1 = 18
led2 = 23
led3 = 17
buzzer = 27
GPIO.setup(led1, GPIO.OUT)
GPIO.setup(led2, GPIO.OUT)
GPIO.setup(led3, GPIO.OUT)
GPIO.setup(buzzer, GPIO.OUT)

def ledOff():
    GPIO.output(led1, False)
    GPIO.output(led2, False)
    GPIO.output(led3, False)
    GPIO.output(buzzer, False)
    sleep(1)

def led1_On():
    GPIO.output(led1, True)
    GPIO.output(led2, False)
    GPIO.output(led3, False)
    GPIO.output(buzzer, False)
    sleep(60)

def led2_Five():
    for i in range(0, 5):
        ledOff()
        GPIO.output(led1, False)
        GPIO.output(led2, True)
        GPIO.output(led3, False)
        GPIO.output(buzzer, True)
        sleep(1)

def led3_On():
    GPIO.output(led1, False)
    GPIO.output(led2, False)
    GPIO.output(led3, True)
    GPIO.output(buzzer, False)
    sleep(60)

def led2_Three():
    for i in range(0, 3):
        ledOff()
        GPIO.output(led1, False)
        GPIO.output(led2, True)
        GPIO.output(led3, False)
        GPIO.output(buzzer, True)
        sleep(1)

while True:
    ledOff()
    led1_On()
    led2_Five()
    ledOff()
    led3_On()
    led2_Three()

GPIO.cleanup()
