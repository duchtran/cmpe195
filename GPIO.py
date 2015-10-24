# Has to run with sudo
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_UP)
#GPIO.setup(24, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

while True:
	if(GPIO.input(23) == 1):
		print("Button 1 pressed") 

GPIO.cleanup()


