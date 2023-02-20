#!/usr/bin/python
import time
from pirc522 import RFID
import RPi.GPIO as GPIO
rdr = RFID()
util = rdr.util()
try:
	while True:
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
				util.auth(rdr.auth_a, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
				util.deauth()
				time.sleep(1)
			else:
				print("idk")
		else:
			print("abc")
except KeyboardInterrupt:
	print('interrupted!')
	GPIO.cleanup()
