from typing import TYPE_CHECKING

# from commands2 import SubsystemBase
from wpilibextra.coroutine.subsystem import SubsystemBase


if TYPE_CHECKING:
	from robot import Robot

import ctre
import wpilib


class Intake(SubsystemBase):
	def __init__(self, robot: "Robot"):
		super().__init__()
		self.robot = robot
		self.motor = ctre.WPI_TalonSRX(6)
		self.has_gamepiece = False

	def stop(self):
		self.run(0)

	def intake(self, speed=0.5):
		speed = abs(speed)
		self.run(speed)

	def hold(self):
		self.intake(0.3)

	def outtake(self, speed=0.25):
		speed = -abs(speed)
		self.run(speed)
		self.has_gamepiece = False
		self.robot.leds.set_mode(self.robot.leds.MODE_OFF)

	def run(self, speed):
		wpilib.SmartDashboard.putNumber("Intake Speed", speed)
		self.motor.set(speed)

	def get_current(self):
		return self.motor.getSupplyCurrent()

	def log(self):
		wpilib.SmartDashboard.putNumber("Intake Current", self.get_current())
		wpilib.SmartDashboard.putBoolean("Has Gamepiece", self.has_gamepiece)
		pass

	def intake_then_hold_coroutine(self):
		self.has_gamepiece = False
		self.intake(1)
		while True:
			for i in range(20):
				yield
				if self.get_current() < 20:
					break
			else:
				self.intake(0.3)
				self.has_gamepiece = True
				self.robot.leds.set_mode(self.robot.leds.MODE_CARRYING)

