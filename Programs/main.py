#!/usr/bin/python

# ------------ LIBRARIES SECTION ------------
import time
import RPi.GPIO as GPIO
# server
import requests
# rfid
from mfrc522 import SimpleMFRC522
# LCD
from rpi_lcd import LCD
# keyboard
from pad4pi import rpi_gpio
# servo driver
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
import board
import busio
import adafruit_pca9685
from adafruit_servokit import ServoKit

# ------------ STARTER PACK STUFF SECTION ------------
i2c = busio.I2C(board.SCL, board.SDA)
pca = adafruit_pca9685.PCA9685(i2c)		# driver
kit = ServoKit(channels=16)				# driver
pca.frequency = 50 						# set frequency for servos driver
card = SimpleMFRC522() 					# rfid
lcd = LCD(address=0x3f) 				# lcd

keyboard = ""							# keyboard input
KEYPAD = [
	["1","2","3","A"],
	["4","5","6","B"],
	["7","8","9","C"],
	["*","0","#","D"]
	]
ROW_PINS = [21, 20, 16, 12] 			# BCM 
COL_PINS = [26, 19, 13, 6] 				# BCM 
factory = rpi_gpio.KeypadFactory()
keypad = factory.create_keypad(keypad=KEYPAD,row_pins=ROW_PINS, col_pins=COL_PINS, gpio_mode=GPIO.BCM)

# ------------ SERVER VARIABLES ------------
server = "0000"			# info from and to the server
code = "2111"
case = 1 			
exit_btns = ("*", "A", "B", "C", "D")

# ------------ TEST SECTION TEMP SECTION ------------
requests.post("http://localhost:8183", "{'code':2111, 'case':0, 'box':0}")
#password = requests.get("http://localhost:8183").text
#print(password)

def key_pressed(key):
	global keyboard
	try:
		keyboard += str(key)
	except ValueError:
		print("F")

def activate_keyboard():
	keypad.registerKeyPressHandler(key_pressed)

def deactive_keyboard():
	keypad.unregisterKeyPressHandler(key_pressed)

def lcd_text(text, num):			# text with space filler
	leng = 16-len(text)
	lcd.text(text + leng*" ", num)

def check_if_wrong_password():
	global keyboard
	if len(keyboard) >= 4:
		if code != keyboard:
			lcd_text("Wrong password!", 1)
			lcd_text("Wait 3 sec >:(", 2)	
			time.sleep(3)				
		keyboard = ""


def lcd_show_card_id():
	print("Card ID: ", str(id))
	lcd_text("Your card ID:", 1)
	lcd_text(str(id), 2)

def lcd_timer(timer):
	for i in range(timer,0,-1):
		lcd_text("Box: " + str(case), 1)
		lcd_text(str(i), 2)
		time.sleep(1)

def lcd_show_password():
	lcd_text("Password: ", 1)
	lcd_text(len(keyboard)*"*", 2)
	
def open_for_x_seconds(timer):
	kit.continuous_servo[case].throttle = 1
	lcd_timer(timer)
	kit.continuous_servo[case].throttle = -1
	time.sleep(1)

def open_box():
	kit.continuous_servo[0].throttle = 1

def close_box():
	kit.continuous_servo[0].throttle = -1

def get_from_server():
	global server, case, code
	server = eval(requests.get("http://localhost:8183").text)
	code, case= str(server['code']), int(server['case'])


def post_info_to_the_server(code: int, case: int, box: str):
	try:
		if box == "can":
			msg = "{'code':" + str(code) + ", 'case':" + str(case) + ", 'box':1}"
		elif box == "cant":
			msg = "{'code':" + str(code) + ", 'case':" + str(case) + ", 'box':0}"
		else:
			raise ValueError
		requests.post("http://localhost:8183", msg)
	except ValueError:
		print("error")

try:
	while str(keyboard) not in exit_btns:
		lcd_text("Hi! ", 1)
		lcd_text("Put your card!", 2)		
		id, text = card.read()
		lcd_show_card_id()	
		if id == 551701029536:
			id = 0
			open_box()			
			post_info_to_the_server(code, case, "can")
			time.sleep(3)		# show 
			activate_keyboard()		
			while str(keyboard) not in exit_btns:		
				#server = eval(requests.get("http://localhost:8183").text)
				get_from_server()
				check_if_wrong_password()
				lcd_show_password()
				time.sleep(1)
				if str(code) == str(keyboard):
					post_info_to_the_server(code, case, "cant")
					deactive_keyboard()
					keyboard = ""
					open_for_x_seconds(10)
					lcd_text("Thats all! ", 1)
					lcd_text("THX!", 2)		
					time.sleep(5)		
					close_box()
					lcd.clear()
					break
			else:
				deactive_keyboard()
		else:
			lcd_text("Wrong card! ", 1)
			lcd_text("Try again!", 2)	
	else:
		deactive_keyboard()
except KeyboardInterrupt:
	lcd.clear()
	print('interrupted!')
except TypeError:
	lcd_text("My processor", 1)
	lcd_text("is broken :(", 2)	
finally:
	if str(keyboard) in exit_btns:
		lcd_text("My job here...", 1)
		lcd_text("...is done", 2)			
	else:
		lcd_text("Bye!", 1)			
		lcd_text("Have a nice day!", 2)
GPIO.cleanup()