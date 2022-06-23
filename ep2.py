import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

seg_a = 16
seg_b = 12
seg_c = 13
seg_d = 6
seg_e = 5
seg_f = 20
seg_g = 21
key = 2
trigger = 23
echo = 24

GPIO.setup(seg_a, GPIO.OUT)
GPIO.setup(seg_b, GPIO.OUT)
GPIO.setup(seg_c, GPIO.OUT)
GPIO.setup(seg_d, GPIO.OUT)
GPIO.setup(seg_e, GPIO.OUT)
GPIO.setup(seg_f, GPIO.OUT)
GPIO.setup(seg_g, GPIO.OUT)
GPIO.setup(key, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(trigger, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)

led_num = 0
led_list = [[1, 1, 1, 1, 1, 1, 0],
            [0, 1, 1, 0, 0, 0, 0],
            [1, 1, 0, 1, 1, 0, 1],
            [1, 1, 1, 1, 0, 0, 1],
            [0, 1, 1, 0, 0, 1, 1],
            [1, 0, 1, 1, 0, 1, 1],
            [1, 0, 1, 1, 1, 1, 1],
            [1, 1, 1, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 0, 1, 1],
            [1, 1, 1, 0, 1, 1, 1],
            [0, 0, 1, 1, 1, 1, 1],
            [1, 0, 0, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 1, 1, 1, 1],
            [1, 0, 0, 0, 1, 1, 1]]

def seg_show():
    seg = led_list[led_num]
    GPIO.output(seg_a, seg[0])
    GPIO.output(seg_b, seg[1])
    GPIO.output(seg_c, seg[2])
    GPIO.output(seg_d, seg[3])
    GPIO.output(seg_e, seg[4])
    GPIO.output(seg_f, seg[5])
    GPIO.output(seg_g, seg[6])

def key_callback(channel):
    global led_num
    led_num = (led_num + 1) % 16
    seg_show()
    pass

GPIO.add_event_detect(key, GPIO.FALLING, callback=key_callback, bouncetime=200)

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
    distance_in = distance_cm / 2.54
    return (distance_cm, distance_in)

while True:
    seg_show()
    print("cm=%.4f \t inches=%.4f" % get_distance())
    time.sleep(3)

GPIO.cleanup()
