from gpiozero import LightSensor
from time import sleep
import pigpio
import time
import random
import os

os.system("sudo pigpiod") 

sensitivity = 0.15
strength = 0.7
len_factor = 10

pi = pigpio.pi()

ldr1 = LightSensor(23)
ldr2 = LightSensor(25)
ldr3 = LightSensor(27)
ldr4 = LightSensor(4)

#R, G, B
wall_1_pins = [22, 17, 24]
wall_2_pins = [6, 13, 5]
wall_3_pins = [16, 12, 20]
wall_4_pins = [26, 19, 21]


def LED_on(wall_pins, R_max, G_max, B_max):

	RED_PIN = wall_pins[0]
	GREEN_PIN = wall_pins[1]
	BLUE_PIN = wall_pins[2]

	r = random.randint(R_max,R_max)
	g = random.randint(G_max,G_max)
	b = random.randint(B_max,B_max)

	setLights(RED_PIN, r)
	setLights(GREEN_PIN, g)
	setLights(BLUE_PIN, b)


def random_LED_on(wall_pins):

	RED_PIN = wall_pins[0]
	GREEN_PIN = wall_pins[1]
	BLUE_PIN = wall_pins[2]

	r = random.randint(0,255)
	g = random.randint(0,255)
	b = random.randint(0,255)

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



def random_light_up(wall_number):
	if wall_number == 1:
		random_LED_on(wall_1_pins)

	elif wall_number == 2:
		random_LED_on(wall_2_pins)

	elif wall_number == 3:
		random_LED_on(wall_3_pins)

	elif wall_number == 4:
		random_LED_on(wall_4_pins)	



def light_off(wall_number):
	if wall_number == 1:
		LED_off(wall_1_pins)

	elif wall_number == 2:
		LED_off(wall_2_pins)

	elif wall_number == 3:
		LED_off(wall_3_pins)

	elif wall_number == 4:
		LED_off(wall_4_pins)	



def wall_hit(wall_number, sensitivity):
	if wall_number == 1:
		while True:
			if ldr1.value < sensitivity:
				return True

	elif wall_number == 2:
		while True:
			if ldr2.value < sensitivity:
				return True

	elif wall_number == 3:
		while True:
			if ldr3.value < sensitivity:
				return True

	elif wall_number == 4:
		while True:
			if ldr4.value < sensitivity:
				return True


def laser_aligned(wall_number, strength):
	if wall_number == 1:
		while True:
			if ldr1.value > strength:
				return True

	elif wall_number == 2:
		while True:
			if ldr2.value > strength:
				return True

	elif wall_number == 3:
		while True:
			if ldr3.value > strength:
				return True

	elif wall_number == 4:
		while True:
			if ldr4.value > strength:
				return True


def setLights(pin, brightness):

	bright = 255
	realBrightness = int(int(brightness) * (float(bright) / 255.0))
	pi.set_PWM_dutycycle(pin, realBrightness)
	

def light_all():

	LED_on(wall_1_pins, 255, 255, 255)
	LED_on(wall_2_pins, 255, 255, 255)
	LED_on(wall_3_pins, 255, 255, 255)
	LED_on(wall_4_pins, 255, 255, 255)


def light_all_color(R, G, B):

	LED_on(wall_1_pins, R, G, B)
	LED_on(wall_2_pins, R, G, B)
	LED_on(wall_3_pins, R, G, B)
	LED_on(wall_4_pins, R, G, B)
	

def turn_off_all():

	LED_off(wall_1_pins)
	LED_off(wall_2_pins)
	LED_off(wall_3_pins)
	LED_off(wall_4_pins)


def blink_color(wait, R, G, B):

	light_all_color(R, G, B)
	time.sleep(wait)
	turn_off_all()
	time.sleep(wait)


def blink(wait):

	light_all()
	time.sleep(wait)
	turn_off_all()
	time.sleep(wait)


def check_align(sensitivity):

        blink_color(1, 255, 0, 0)
        
        LED_on(wall_1_pins, 255, 0, 0)
        if laser_aligned(1, strength):
                LED_on(wall_1_pins, 0, 255, 0)

        LED_on(wall_2_pins, 255, 0, 0)
        if laser_aligned(2, strength):
                LED_on(wall_2_pins, 0, 255, 0)

        LED_on(wall_3_pins, 255, 0, 0)
        if laser_aligned(3, strength):
                LED_on(wall_3_pins, 0, 255, 0)

        LED_on(wall_4_pins, 255, 0, 0)
        if laser_aligned(4, strength):
                LED_on(wall_4_pins, 0, 255, 0)

        blink_color(1, 0, 255, 0)

        


# START GAME

turn_off_all()
time.sleep(1)

# check_align(sensitivity)

blk_wait = 0.5
blink(blk_wait)
blink(blk_wait)
blink(blk_wait)

circuit_len = 60*len_factor
timeout = time.time() + circuit_len   # minutes from now
wall_count = 0

print("TIME LEFT: "+str(circuit_len))
  
while True:

	if time.time() > timeout:
		break

	walls = [1,2,3,4]
	random_wall = random.choice(walls)
	random_light_up(random_wall)

	if wall_hit(random_wall, sensitivity):

		time_elapsed = time.time() - timeout
		time_left = 0 - time_elapsed
		print("TIME LEFT: "+str(time_left))

		wall_count += 1
		light_off(random_wall)

light_all()
print("WALLS HIT: " + str(wall_count))
