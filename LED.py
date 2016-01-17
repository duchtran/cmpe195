import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setup(36,GPIO.OUT)


while 1:
	GPIO.output(36, GPIO.HIGH);
	time.sleep(1);
	GPIO.output(36, GPIO.LOW);
	time.sleep(1);

