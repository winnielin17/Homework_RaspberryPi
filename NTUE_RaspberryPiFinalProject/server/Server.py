import RPi.GPIO as GPIO
import adafruit_dht
import board
import requests
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

dht = adafruit_dht.DHT22(board.D4)
TARGET_URL = 'localhost'

led1 = 17
led2 = 18
led3 = 23
GPIO.setup(led1, GPIO.OUT)
GPIO.setup(led2, GPIO.OUT)
GPIO.setup(led3, GPIO.OUT)

def ledOff():
    GPIO.output(led1, False)
    GPIO.output(led2, False)
    GPIO.output(led3, False)
    sleep(1)

def led1_On():
    GPIO.output(led1, True)
    GPIO.output(led2, False)
    GPIO.output(led3, False)
    sleep(3)

def led2_On():
    GPIO.output(led1, False)
    GPIO.output(led2, True)
    GPIO.output(led3, False)
    sleep(3)

def led3_On():
    GPIO.output(led1, False)
    GPIO.output(led2, False)
    GPIO.output(led3, True)
    sleep(3)

def sent():
    r = requests.get('http://{0}/LogRecord_GET.php?temp={1}&wet={2}&light={3}'.format(
        TARGET_URL, temp, humid, light))
    print("Server Return Code:", r.status_code)
    print(r.text)

while True:
    try:
        temp = dht.temperature
        humid = dht.humidity
        light = 0
        ledOff()
        print("Temp: {:.2f}*C  Humidity: {:.2f}% ".format(temp, humid))

        if 19 <= temp <= 28 and humid < 80:
            light = 3
            print("Light:", light)
            sent()
            led3_On()
        elif ((temp < 19 or temp > 28) and humid < 80) or (19 <= temp <= 28 and humid >= 80):
            light = 2
            print("Light:", light)
            sent()
            led2_On()
        elif (temp < 19 or temp > 28) and humid >= 80:
            light = 1
            print("Light:", light)
            sent()
            led1_On()
    except RuntimeError as error:
        print(error.args[0])
        sleep(1)
        continue
    except Exception as error:
        dht.exit()
        GPIO.cleanup()
        raise error
