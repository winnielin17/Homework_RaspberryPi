import spidev
import time
import os
import sys
import smbus2
from RPLCD.i2c import CharLCD

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000

def ReadADC(ch):
    if (ch > 7) or (ch < 0):
        return -1
    adc = spi.xfer2([1, (8 + ch) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

light_ch = 0
vrx_ch = 1
vry_ch = 2
swt_ch = 3

sys.modules['smbus'] = smbus2

lcd = CharLCD('PCF8574', address=0x27, port=1, backlight_enabled=True)

try:
    print('Press CTRL + C to quit')
    lcd.clear()
    while True:
        light_data = ReadADC(light_ch)
        vrx_pos = ReadADC(vrx_ch)
        vry_pos = ReadADC(vry_ch)
        swt_val = ReadADC(swt_ch)

        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string("L:" + str(light_data))
        lcd.cursor_pos = (0, 7)
        lcd.write_string("S:" + str(swt_val))
        lcd.cursor_pos = (1, 0)
        lcd.write_string("X:" + str(vrx_pos))
        lcd.cursor_pos = (1, 7)
        lcd.write_string("Y:" + str(vry_pos))

        time.sleep(0.5)

        if (light_data > 700 or light_data < 200 or
            vry_pos < 50 or vry_pos > 950 or
            vrx_pos < 50 or vrx_pos > 950 or
            swt_val < 50):
            lcd.clear()

        if light_data > 700:
            lcd.cursor_pos = (0, 0)
            lcd.write_string("Light")
        elif light_data < 200:
            lcd.cursor_pos = (0, 0)
            lcd.write_string("Dark")

        if vry_pos < 50 and vrx_pos < 50:
            lcd.cursor_pos = (1, 0)
            lcd.write_string("UP LEFT")
        elif vry_pos < 50 and vrx_pos > 950:
            lcd.cursor_pos = (1, 0)
            lcd.write_string("UP RIGHT")
        elif vry_pos > 950 and vrx_pos < 50:
            lcd.cursor_pos = (1, 0)
            lcd.write_string("DOWN LEFT")
        elif vry_pos > 950 and vrx_pos > 950:
            lcd.cursor_pos = (1, 0)
            lcd.write_string("DOWN RIGHT")
        elif vry_pos < 50:
            lcd.cursor_pos = (1, 0)
            lcd.write_string("UP")
        elif vry_pos > 950:
            lcd.cursor_pos = (1, 0)
            lcd.write_string("DOWN")
        elif vrx_pos < 50:
            lcd.cursor_pos = (1, 0)
            lcd.write_string("LEFT")
        elif vrx_pos > 950:
            lcd.cursor_pos = (1, 0)
            lcd.write_string("RIGHT")
        elif swt_val < 50:
            lcd.cursor_pos = (1, 0)
            lcd.write_string("PRESSED")

        time.sleep(0.5)
except KeyboardInterrupt:
    print('Closed Program')
finally:
    lcd.clear()
