import RPi.GPIO as GPIO
import time
import sys
import smbus2
from RPLCD.i2c import CharLCD

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

trigger = 23
echo = 24
buzzer = 18

GPIO.setup(trigger, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)
GPIO.setup(buzzer, GPIO.OUT)

Do = 523
Re = 587
Mi = 659
Fa = 698
So = 784

song = [Mi, Mi, Fa, So, So, Fa, Mi, Re, Do, Do, Re, Mi]

def trigger_send():
    GPIO.output(trigger, True)
    time.sleep(0.001)
    GPIO.output(trigger, False)

def echo_wait(value, timeout):
    count = timeout
    while GPIO.input(echo) != value and count > 0:
        count = count - 1

def get_distance():
    trigger_send()
    echo_wait(True, 5000)  # 等於True時記錄開始時間
    start = time.time()
    echo_wait(False, 5000)  # 等於False時記錄結束時間
    end = time.time()
    pulse_len = end - start
    distance_cm = pulse_len * 340 * 100 / 2
    return distance_cm

def play(pitch, sec):
    half_pitch = (1 / pitch) / 2
    t = int(pitch * sec)
    for i in range(t):
        GPIO.output(buzzer, GPIO.HIGH)
        time.sleep(half_pitch)
        GPIO.output(buzzer, GPIO.LOW)
        time.sleep(half_pitch)

sys.modules['smbus'] = smbus2

lcd = CharLCD('PCF8574', address=0x27, port=1, backlight_enabled=True)

try:
    print('Press CTRL + C to quit')
    lcd.clear()
    while True:
        dist_cm = get_distance()
        dist_in = dist_cm / 2.54

        lcd.cursor_pos = (0, 0)
        lcd.write_string("cm=%.4f" % dist_cm)
        lcd.cursor_pos = (1, 0)
        lcd.write_string("inches=%.4f" % dist_in)

        if dist_cm < 5:
            for s in song:
                play(s, 0.5)
            play(Mi, 0.75)
            play(Re, 0.25)
            play(Re, 1)
            for s in song:
                play(s, 0.5)
            play(Re, 0.75)
            play(Do, 0.25)
            play(Do, 1)

        time.sleep(1)
except KeyboardInterrupt:
    print('Closed Program')
finally:
    lcd.clear()
    GPIO.cleanup()
