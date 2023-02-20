import board
import busio
import time
import adafruit_pca9685
from adafruit_motor import servo
from adafruit_servokit import ServoKit
print(type(board.SCL))
i2c = busio.I2C(board.SCL, board.SDA)
pca = adafruit_pca9685.PCA9685(i2c)


### Blink LED on channel 0

#led_channel = pca.channels[0]

#pca.frequency = 60
#try:
#	while True:
#		led_channel.duty_cycle = 1000
#		time.sleep(2)
#		led_channel.duty_cycle = 20
#		time.sleep(2)
		#for i in range(0xffff):
	#		led_channel.duty_cycle = i
	#		time.sleep(0.1)
#except KeyboardInterrupt:
#	pass

### Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.

kit = ServoKit(channels=8)
pca.frequency = 50

kit.servo[0].angle = 180
kit.continuous_servo[1].throttle = 1
time.sleep(1)
kit.continuous_servo[1].throttle = -1
time.sleep(1)
kit.servo[0].angle = 0
kit.continuous_servo[1].throttle = 0

