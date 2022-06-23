import sys
import smbus
from RPLCD.i2c import CharLCD
import adafruit_dht
import board
import requests
import time
import RPi.GPIO as GPIO

sys.modules['smbus'] = smbus

TARGET_URL = 'localhost'

# Initial the dht device, with data pin connected to GPIO4:
dhtDevice = adafruit_dht.DHT22(board.D4)

lcd = CharLCD('PCF8574', address=0x27, port=1, backlight_enabled=True)
lcd.clear()

while True:
    try:
        # Print the values to the serial port
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        temperature_f = round(temperature_f, 2)
        humidity = dhtDevice.humidity

        print("Temp: {:.2f}*C / {:.2f}*F    Humidity: {:.2f}% \n".format(
            temperature_c, temperature_f, humidity))
        r = requests.get('http://{0}/LogRecord_GET.php?TEMP_C={1}&TEMP_F={2}&HUMD={3}'.format(
            TARGET_URL, temperature_c, temperature_f, humidity))
        print("Server Return Code :", r.status_code)
        print(r.text)
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string("{:.2f}*C {:.2f}*F".format(temperature_c, temperature_f))
        lcd.cursor_pos = (1, 0)
        lcd.write_string("Humidity: {0:.2f}%".format(humidity))
        time.sleep(2)

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2)
        continue
    except Exception as error:
        dhtDevice.exit()
        GPIO.cleanup()
        raise error
