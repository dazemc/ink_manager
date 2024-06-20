#!/bin/py
# 0: busy, 1:
import RPi.GPIO as GPIO
import sys
GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.IN)
sys.exit(GPIO.input(24))
