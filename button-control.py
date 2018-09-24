#!/usr/bin/env python

from __future__ import print_function
import sys

import RPi.GPIO as GPIO
import time
from chromatron import *


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

GPIO.setwarnings(False)

# use P1 header pin numbering convention
GPIO.setmode(GPIO.BOARD)

class Button(object):
    """Button w/ a switch + LED"""

    def __init__(self, switch_pin, led_pin):
        # light state tracking
        self.light_state = False
        self.blinking = False

        # button debouncing
        self.prev_button_sample = False
        self.button_sample = False

        # button state tracking
        self.button_state = False

        # hw resources
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
        self.prev_button_sample = self.button_sample
        self.button_sample = not GPIO.input(self.switch_pin)

        pushed_now = False
        if self.prev_button_sample == self.button_sample:
            pushed_now = self.button_sample

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

group.stop_vm()
group.set_all_hsv(0, 0, 0) # off

for fname in ["rainbow.fxb", "chaser.fxb", "emergency.fxb", "lightning.fxb"]:
    with open(fname) as f: fdata = f.read()
    group.put_file(fname, fdata)

# group.load_vm('rainbow.fx', False)
# group.load_vm('chaser.fx', False)
# group.load_vm('emergency.fx', False)
# group.load_vm('lightning.fx', False)

eprint("starting loop")

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

    switch_script("lightning.fxb")

    while True:
        if blue.update():
            # emergency.fxb
            switch_script("emergency.fxb")
            eprint("Blue pushed")
        if red.update():
            # chaser.fxb
            switch_script("chaser.fxb")
            eprint("Red pushed")
        if yellow.update():
            # rainbow.fxb
            switch_script("rainbow.fxb")
            eprint("Yellow pushed")
        if green.update():
            # lightning.fxb
            switch_script("lightning.fxb")
            eprint("Green pushed")

        time.sleep(0.05)
except KeyboardInterrupt:
    eprint("exiting")

eprint("done")

GPIO.cleanup()

