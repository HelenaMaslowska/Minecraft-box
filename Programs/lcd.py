#!/usr/bin/python

from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

lcd = LCD(address=0x3f)

def safe_exit(signum, frame):
    exit(1)

try:
    signal(SIGTERM, safe_exit)
    signal(SIGHUP, safe_exit)

    lcd.text("Hello,", 1)
    lcd.text("Raspberry Pi!", 2)

    pause()

except KeyboardInterrupt:
    pass

finally:
    lcd.clear()
