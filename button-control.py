#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
from chromatron import *

# use P1 header pin numbering convention
GPIO.setmode(GPIO.BOARD)

class Button(object):
    """Button w/ a switch + LED"""

    def __init__(self, switch_pin, led_pin):
        self.light_state = False
        self.blinking = False
        self.button_state = False
        self.switch_pin = switch_pin
        self.led_pin = led_pin
        GPIO.setup(self.switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.led_pin, GPIO.OUT)
        self.light_off()
        print("setup one button")

    def light_toggle(self):
        self.light_state = not self.light_state
    def light_on(self):
        self.light_state = True
        self.light_output()
    def light_off(self):
        self.light_state = False
        self.light_output()

    def light_output(self):
        if self.blinking:
            GPIO.output(self.led_pin, not GPIO.input(self.led_pin))
        else:
            if self.light_state:
                GPIO.output(self.led_pin, GPIO.HIGH)
            else:
                GPIO.output(self.led_pin, GPIO.LOW)

    def update_button_state(self):
        """True is pushed"""
        pushed_now = not GPIO.input(self.switch_pin)
        if self.button_state and pushed_now:
            self.button_was_held_down()
        elif not self.button_state and pushed_now:
            self.button_state = True
            self.button_was_pushed()
        elif self.button_state and not pushed_now:
            self.button_state = False
            self.button_was_released()
        else:
            self.button_was_left_up()

        return pushed_now

    def button_was_held_down(self):
        self.blinking = True
    def button_was_pushed(self):
        self.light_toggle()
    def button_was_released(self):
        self.blinking = False
    def button_was_left_up(self):
        pass

    def update(self):
        b = self.update_button_state() 
        self.light_output()

        if b:
            return True
        else:
            return False


# switch pin - led pin
blue   = Button(13, 11)
red    = Button(15, 16)
yellow = Button(37, 36)
green  = Button(31, 29)

# # Set up the GPIO channels - one input and one output
# GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# GPIO.setup(11, GPIO.OUT)
#
# GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# GPIO.setup(16, GPIO.OUT)

group = DeviceGroup('kitchen')
group.dimmer = 1.0
group.load_vm('rainbow.fx', False)
group.load_vm('chaser.fx', False)
group.load_vm('emergency.fx', False)
group.load_vm('lightning.fx', False)

print("starting loop")

def switch_script(name):
    group.stop_vm()
    group.set_key('vm_prog', name)
    group.start_vm()

try:
    blue.light_on()
    time.sleep(0.33)
    blue.light_off()
    red.light_on()
    time.sleep(0.33)
    red.light_off()
    green.light_on()
    time.sleep(0.33)
    green.light_off()
    yellow.light_on()
    time.sleep(0.33)
    yellow.light_off()

    while True:
        if blue.update():
            # emergency.fxb
            switch_script("emergency.fxb")
            print("Blue pushed")
        if red.update():
            # chaser.fxb
            switch_script("chaser.fxb")
            print("Red pushed")
        if yellow.update():
            # rainbow.fxb
            switch_script("rainbow.fxb")
            print("Yellow pushed")
        if green.update():
            # lightning.fxb
            switch_script("lightning.fxb")
            print("Green pushed")

        time.sleep(0.05)
except KeyboardInterrupt:
    print("exiting")

print("done")

GPIO.cleanup()

