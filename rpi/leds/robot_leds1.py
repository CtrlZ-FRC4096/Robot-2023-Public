# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple test for NeoPixels on Raspberry Pi
import os
import sys
import time
import board
import keyboard
import neopixel
import ntcore


# Roborio IP
#ROBORIO_IP = 'roborio-4096-frc.local'
ROBORIO_IP = '10.40.96.2'

# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
LED1_PIN = board.D18
LED2_PIN = board.D12

# The number of NeoPixels
NUM_LEDS = 14
#NUM_LEDS = 29

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

strip1 = neopixel.NeoPixel(
    LED1_PIN, NUM_LEDS, brightness=1.0, auto_write=False, pixel_order=ORDER
)
strip2 = neopixel.NeoPixel(
    LED2_PIN, NUM_LEDS, brightness=1.0, auto_write=False, pixel_order=ORDER
)

# LED pattern modes to cycle through
MODE_OFF      = 'off'
MODE_CONE     = 'cone'
MODE_CUBE     = 'cube'
MODE_CARRYING = 'carrying'
MODE_WAITING  = 'waiting'

MODES = [
    MODE_OFF,
    MODE_CONE,
    MODE_CUBE,
    MODE_CARRYING,
]

COLOR_PURPLE   = (100, 0, 255)
COLOR_YELLOW   = (255, 180, 0)
COLOR_WHITE    = (255, 255, 255)
COLOR_ORANGE   = (255, 40, 0)
COLOR_BLUE     = (0, 0, 255)


def pattern_scroll(strips, colors, steps=5):
    multiplier = 1.0 - 1.0 / steps
    multiplier = min(multiplier, 0.75)

    for color in colors:
        clear_strips(strips)
        pos = 0

        while pos - steps < NUM_LEDS:
            cur_color = list(color)

            for n in range(steps):
                i = pos - n
                if i < 0 or i >= NUM_LEDS:
                    continue

                for strip in strips:
                    strip[i] = cur_color

                cur_color = tuple([int(c * multiplier) for c in cur_color])
                #print('pos =', pos, 'i =', i, 'n =', n, 'mult = {0:.2f}'.format(multiplier), 'color =', cur_color)

            if i > 0:
                for strip in strips:
                    strip[i-1] = (0,0,0)

            for strip in strips:
                strip.write()

            time.sleep(.015)

            pos += 1


def pattern_flash(strip, color):
    strip.fill(color)
    strip.write()
    time.sleep(0.25)
    strip.fill((0,0,0))
    strip.write()
    time.sleep(0.25)

def pattern_pulse(strip, colors):
    for color in colors:
        cur_color = list(color)
        steps = 125
        multiplier = 1.0 - 100 / steps / 100

        for i in range(steps):
            cur_color = tuple([int(c * multiplier) for c in cur_color])

            avg = sum(cur_color) / 3.0

            if avg < 20:
                cur_color = list(color)

            strip.fill(cur_color)
            strip.write()


def get_robot_intake_mode(nt_inst):
    """
    Queries networktables on roborio to get driver's desired LED mode.
    If not set or no connection is made, defaults to 0, which is MODE_OFF
    """
    sd = nt_inst.getTable("SmartDashboard")
    intake_mode = sd.getString("led_mode", MODE_WAITING)

    return intake_mode


def clear_strips(strips):
    for strip in strips:
        strip.fill((0,0,0))

        while True:
            try:
                strip.write()
                break
            except RuntimeError:
                time.sleep(1)


### MAIN ###

print('STARTING LEDs SCRIPT:', __file__)

# Start networktables client
nt_inst = ntcore.NetworkTableInstance.getDefault()
identity = os.path.basename(__file__)
nt_inst.startClient4(identity)
nt_inst.setServer(ROBORIO_IP)
nt_robot = nt_inst.getTable('robot')

#mode_idx = 0
last_mode = ''

while True:
    mode = get_robot_intake_mode(nt_inst)
    #mode = MODES[mode_idx]
    #mode = nt_robot.getString('led_mode', MODE_CONE)
    if mode != last_mode:
        print(mode)
        last_mode = mode

    try:
        # Check for keypress
        if keyboard.is_pressed('esc'):
            break

        #if keyboard.is_pressed('space'):
            #mode_idx += 1
            #if mode_idx == len(MODES):
                #mode_idx = 0

            #time.sleep(.1)

        # Run appropriate mode
        if mode == MODE_OFF:
            #print('OFF')
            clear_strips((strip1, strip2))
        elif mode == MODE_CUBE:
            #print('CUBE')
            pattern_pulse(strip1, [COLOR_PURPLE])
            pattern_pulse(strip2, [COLOR_PURPLE])
        elif mode == MODE_CONE:
            #print('CONE')
            pattern_pulse(strip1, [COLOR_YELLOW])
            pattern_pulse(strip2, [COLOR_YELLOW])
        elif mode == MODE_CARRYING:
            pattern_flash(strip1, COLOR_WHITE)
            pattern_flash(strip2, COLOR_WHITE)
        elif mode == MODE_WAITING:
            pattern_scroll([strip1, strip2], [COLOR_ORANGE, COLOR_BLUE], steps=16)
            #pattern_scroll([strip1], [COLOR_ORANGE, COLOR_BLUE], steps=16)
        else:
            pass

    except KeyboardInterrupt:
        break

# Exited, so turn LEDs off
#clear_strips((strip1, strip2))

sys.exit(0)
