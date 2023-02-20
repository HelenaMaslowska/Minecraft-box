#!/usr/bin/python
import time
from pirc522 import RFID
import RPi.GPIO as GPIO
from rpi_lcd import LCD
from pad4pi import rpi_gpio
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
stringi = ""
rdr = RFID()
lcd = LCD(address=0x3f)
# util = rdr.util()
KEYPAD = [
	["1","2","3","A"],
	["4","5","6","B"],
	["7","8","9","C"],
	["*","0","#","D"]
	]
ROW_PINS = [40, 38, 36, 32] # BCM 
COL_PINS = [37, 35, 33, 31] # BCM 
factory = rpi_gpio.KeypadFactory()
keypad = factory.create_keypad(keypad=KEYPAD,row_pins=ROW_PINS, col_pins=COL_PINS, gpio_mode=GPIO.BOARD) #stworzenie klasy klawiatury membranowej
def key_pressed(key):
    global stringi
    try:
        stringi += str(key)
    except ValueError:
        print("DIPA")
keypad.registerKeyPressHandler(key_pressed)
try:
	while True:
		lcd.clear()
		print("hello there")
		rdr.wait_for_tag()
		print("i waited for tag")
		(error, data) = rdr.request()
		print("nice request bro")
		if not error:
			print("\nDetected")
			(error, uid) = rdr.anticoll()
			if not error:
				print("Card read UID: " + str(uid))
				# Set tag as used in util. This will call RFID.select_tag(uid)
				util.set_tag(uid)
				lcd.text(stringi, 1)
				util.auth(rdr.auth_a, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
				util.deauth()
				time.sleep(1)
			else:
				print("idk")
		else:
			print("abc")
except KeyboardInterrupt:
	lcd.clear()
	keypad.cleanup()
	print('interrupted!')
	GPIO.cleanup()
