from time import sleep
import sys
from mfrc522 import SimpleMFRC522
from rpi_lcd import LCD
import RPi.GPIO as GPIO
from pad4pi import rpi_gpio

KEYPAD = [
        ["1","2","3","A"],
        ["4","5","6","B"],
        ["7","8","9","C"],
        ["*","0","#","D"]
        ]
ROW_PINS = [40, 38, 36, 32] # BCM
COL_PINS = [37, 35, 33, 31] # BCM

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

reader = SimpleMFRC522()
lcd = LCD(address=0x3f)
factory = rpi_gpio.KeypadFactory()

keypad = factory.create_keypad(keypad=KEYPAD,row_pins=ROW_PINS, col_pins=COL_PINS, gpio_mode=GPIO.BOARD) #stworzenie klasy klawiatury
stringi = ""

# util = rdr.util()

def key_pressed(key):
    global stringi
    try:
        stringi += str(key)
    except ValueError:
        print("no nie dziala")

keypad.registerKeyPressHandler(key_pressed)

try:
	lcd.clear()
	while True:
		print("Hold a tag near the reader")
		id, text = reader.read()
		print("ID: %s\nText: %s" % (id,text))
		lcd.text(stringi, 1)
		sleep(1)
		
except KeyboardInterrupt:
	lcd.clear()
	GPIO.cleanup()
	keypad.cleanup()
	print('interrupted!')
	GPIO.cleanup()
