from typing import TYPE_CHECKING

# from commands2 import SubsystemBase
from wpilibextra.coroutine.subsystem import SubsystemBase

if TYPE_CHECKING:
	from robot import Robot

import wpilib

# Constants
PWM_PORT		= 9
NUM_LEDS		= 14


class LEDs(SubsystemBase):
	# LED pattern modes to cycle through
	MODE_OFF		= 'off'
	MODE_CONE		= 'cone'
	MODE_CUBE		= 'cube'
	MODE_CARRYING	= 'carrying'
	MODE_WAITING    = 'waiting'

	# RGB Colors
	COLOR_PURPLE   = (100, 0, 255)
	COLOR_YELLOW   = (255, 180, 0)
	COLOR_WHITE    = (255, 255, 255)
	COLOR_ORANGE   = (255, 40, 0)
	COLOR_BLUE     = (0, 0, 255)

	def __init__(self, robot: "Robot"):
		super().__init__()
		self.robot = robot

		self.mode = self.MODE_WAITING

		self.led = wpilib.AddressableLED(port = PWM_PORT)
		self.led.setLength(NUM_LEDS)

		# Initialize our LED color data list
		self.data = [ ]
		for i in range(NUM_LEDS):
			self.data.append(wpilib.AddressableLED.LEDData(0, 0, 0))

		self.led.setData(self.data)
		self.led.start()

		# States & timers related to patterns below
		self.timer1 = wpilib.Timer()
		self.timer1.start()
		self.flash_on = True
		self.pulse_color_idx = 0
		self.pulse_color = (0,0,0)
		self.scroll_color_idx = 0
		self.scroll_color = (0,0,0)
		self.scroll_pos = 0


	def stop(self):
		pass
		# self.robot.nt_robot.putString('led_mode', self.MODE_OFF)

	def get_mode(self) -> str:
		return self.mode

	def set_mode(self, mode):
		self.mode = mode
		self.robot.nt_robot.putString('led_mode', mode)

	def fill(self, color):
		for led in self.data:
			led.setRGB(*color)

		self.led.setData(self.data)

	def clear(self):
		self.fill((0, 0, 0))
		self.led.setData(self.data)

	def pattern_scroll(self, colors, steps=8):
		multiplier = 0.7

		if self.scroll_color == (0,0,0):
			self.scroll_color = list(colors[self.scroll_color_idx])

		# Start by setting cur_color to scroll_color
		cur_color = tuple([int(c * multiplier) for c in self.scroll_color])
		i = 0

		for n in range(steps):
			# print('cur_color =', cur_color)
			i = self.scroll_pos - n

			if i < 0 or i >= NUM_LEDS:
				continue

			self.data[i].setRGB(*cur_color)

			# Fade cur_color a little
			cur_color = tuple([int(c * multiplier) for c in cur_color])

		if i > 0:
			self.data[i-1].setRGB(0, 0, 0)

		self.led.setData(self.data)

		self.scroll_pos += 1

		if self.scroll_pos - steps >= NUM_LEDS:
			self.scroll_color = (0,0,0)
			self.scroll_pos = 0
			self.scroll_color_idx += 1

			if self.scroll_color_idx == len(colors):
				self.scroll_color_idx = 0


	def pattern_pulse(self, colors):
		# Arbitrary amount to fade color each cycle
		multiplier = 0.7

		if self.pulse_color == (0,0,0):
			self.pulse_color = list(colors[self.pulse_color_idx])

		self.pulse_color = tuple([int(c * multiplier) for c in self.pulse_color])
		self.fill(self.pulse_color)

		if sum(self.pulse_color) / 3.0 < 20:
			# Move to next color
			self.pulse_color == (0,0,0)
			self.pulse_color_idx += 1

			if self.pulse_color_idx == len(colors):
				self.pulse_color_idx = 0


	def pattern_flash(self, color):
		if self.timer1.hasElapsed(0.25):
			if self.flash_on:
				self.clear()
			else:
				self.fill(color)

			self.flash_on = not self.flash_on
			self.timer1.reset()

	def periodicX(self):
		# Set colors for current LED mode
		if self.mode == self.MODE_OFF:
			self.clear()

		elif self.mode == self.MODE_CUBE:
			self.pattern_pulse([self.COLOR_PURPLE])
			self.pattern_pulse([self.COLOR_PURPLE])

		elif self.mode == self.MODE_CONE:
			self.pattern_pulse([self.COLOR_YELLOW])
			self.pattern_pulse([self.COLOR_YELLOW])

		elif self.mode == self.MODE_CARRYING:
			self.pattern_flash(self.COLOR_WHITE)
			self.pattern_flash(self.COLOR_WHITE)

		elif self.mode == self.MODE_WAITING:
			self.pattern_scroll([self.COLOR_ORANGE, self.COLOR_BLUE])

		else:
			pass


	def log(self):
		wpilib.SmartDashboard.putString("LEDs Mode", self.get_mode())
