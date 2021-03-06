#!/usr/bin/env python

from __future__ import print_function
import sys
import os

import RPi.GPIO as GPIO
import time
import datetime

from chromatron import DeviceGroup

from Adafruit_IO import MQTTClient

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
_name, device = group.items()[0]

device.dimmer = 1.0

device.stop_vm()
device.set_all_hsv(0, 0, 0) # off

for fname in ["rainbow.fxb", "chaser.fxb", "emergency.fxb", "lightning.fxb", "mini.fxb"]:
    with open(fname) as f: fdata = f.read()
    device.put_file(fname, fdata)

# device.load_vm('rainbow.fx', False)
# device.load_vm('chaser.fx', False)
# device.load_vm('emergency.fx', False)
# device.load_vm('lightning.fx', False)

eprint("starting loop")

def switch_script(name):
    device.stop_vm()
    device.set_key('vm_prog', name)
    device.start_vm()

def mqtt_connected(client):
    eprint('mqtt connected ok')
    client.subscribe('dad-loc')
def mqtt_disconnected(client):
    eprint('mqtt disconnected')
def mqtt_message(client, feed_id, payload):
    eprint('mqtt message {}'.format(payload))
    if payload == 'work exited':
        switch_script('mini.fxb')

IO_USERNAME=os.environ['IO_USERNAME']
IO_API_KEY=os.environ['IO_API_KEY']

mqtt_client = MQTTClient(IO_USERNAME, IO_API_KEY)
mqtt_client.on_connect = mqtt_connected
mqtt_client.on_disconnect = mqtt_disconnected
mqtt_client.on_message = mqtt_message
mqtt_client.connect()
mqtt_client.loop_background()

dimmer_update_rate = datetime.timedelta(minutes=1)
last_dimmer_update_time = datetime.datetime.now()

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

        if datetime.datetime.now() - last_dimmer_update_time > dimmer_update_rate:
            last_dimmer_update_time = datetime.datetime.now()
            print('checking time for dimming')
            # utc time originally, so 0 == 1800 local
            # dimmer switch times should be about 9pm and 9am,
            # 2100 local -> 0300 utc
            # 0900 local -> 1500 utc
            # so dim when hour between 0200 and 1200
            h = last_dimmer_update_time.hour
            if device.dimmer > 0.10 and (h >= 3 and h < 15):
                device.dimmer = 0.10
                print('should be dim now')
            elif device.dimmer < 1.0 and not (h >= 3 and h < 15):
                device.dimmer = 1.0
                print('should be bright now')
            else:
                print('no change - dimmer:{} hour:{}'.format(device.dimmer, last_dimmer_update_time.hour))

        time.sleep(0.05)

except KeyboardInterrupt:
    eprint("exiting")

eprint("done")

GPIO.cleanup()

