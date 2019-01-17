from gpiozero import LightSensor
from time import sleep
import pigpio
import time
import random


pi = pigpio.pi()

#R, G, B
wall_1_pins = [17, 22, 24]
wall_2_pins = [26, 19, 21]
wall_3_pins = [16, 12, 20]
wall_4_pins = [6, 5, 13]



def LED_on(wall_pins):

	RED_PIN = wall_pins[0]
	GREEN_PIN = wall_pins[1]
	BLUE_PIN = wall_pins[2]

	r = 255.0
	g = 255.0
	b = 255.0

	setLights(RED_PIN, r)
	setLights(GREEN_PIN, g)
	setLights(BLUE_PIN, b)



def LED_off(wall_pins):

	RED_PIN = wall_pins[0]
	GREEN_PIN = wall_pins[1]
	BLUE_PIN = wall_pins[2]

	r = 0.0
	g = 0.0
	b = 0.0

	setLights(RED_PIN, r)
	setLights(GREEN_PIN, g)
	setLights(BLUE_PIN, b)



def light_up(wall_number):
	if wall_number == 1:
		LED_on(wall_1_pins)

	elif wall_number == 2:
		LED_on(wall_2_pins)

	elif wall_number == 3:
		LED_on(wall_3_pins)

	elif wall_number == 4:
		LED_on(wall_4_pins)	



def light_off(wall_number):
	if wall_number == 1:
		LED_off(wall_1_pins)

	elif wall_number == 2:
		LED_off(wall_2_pins)

	elif wall_number == 3:
		LED_off(wall_3_pins)

	elif wall_number == 4:
		LED_off(wall_4_pins)	


def setLights(pin, brightness):

	bright = 255
	realBrightness = int(int(brightness) * (float(bright) / 255.0))
	pi.set_PWM_dutycycle(pin, realBrightness)



def light_all():
	LED_on(wall_1_pins)
	LED_on(wall_2_pins)
	LED_on(wall_3_pins)
	LED_on(wall_4_pins)



def turn_off_all():
	LED_off(wall_1_pins)
	LED_off(wall_2_pins)
	LED_off(wall_3_pins)
	LED_off(wall_4_pins)



def blink():

	light_all()
	time.sleep(1)

	turn_off_all()
	time.sleep(1)

for i in range(0,250):
	

# START GAME

blink()
blink()
blink()

circuit_len = 60
sensitivity = 0.1

timeout = time.time() + circuit_len*1   # 1 minutes from now
wall_count = 0


print("TIME LEFT: "+str(circuit_len))

while time.time() > timeout:

	walls = [1,2,3,4]
	random_wall = random.choice(walls)
	light_up(random_wall)

	if wall_hit(random_wall, sensitivity):

		time_elapsed = time.time() - timeout
		time_left = circuit_len - time_elapsed
		print("TIME LEFT: "+str(time_left))

		wall_count += 1
		light_off(random_wall)


light_all()
print("WALLS HIT: " + wall_count)
