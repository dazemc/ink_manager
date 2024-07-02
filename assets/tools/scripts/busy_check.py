"""Script for checking idle state of e-paper device
    """
#!/bin/py
# 0: busy, 1: idle
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.IN)
print(GPIO.input(24))
