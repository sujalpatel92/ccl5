import RPi.GPIO as gpio
gpio.setmode(gpio.BOARD)
gpio.setup(11, gpio.OUT)
gpio.output(11,gpio.LOW)
