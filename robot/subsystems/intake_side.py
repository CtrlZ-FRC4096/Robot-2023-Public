from typing import TYPE_CHECKING
if TYPE_CHECKING:
	from robot import Robot

# from commands2 import SubsystemBase
from wpilibextra.coroutine.subsystem import SubsystemBase
import ctre
import wpilib
import wpimath
import wpimath.controller
from wpimath.trajectory import TrapezoidProfile

class Intake_Side(SubsystemBase):
	def __init__(self, robot: "Robot"):
		super().__init__()
		self.robot = robot
		self.hatch_motor = ctre.WPI_TalonSRX(7)
		# self.encoder = wpilib.DutyCycleEncoder(-1)
		self.intake_motor = ctre.WPI_TalonFX(42)
		self.has_gamepiece = False
		self.pid_controller = wpimath.controller.ProfiledPIDController(
			Kp=0.32, Ki=0, Kd=0, constraints = TrapezoidProfile.Constraints(100000,3000)
		)
		self.target_angle = 90

	def stop(self):
		self.hatch_motor.set(0)
		self.intake_motor.set(0)

	def intake(self, speed = .3):
		self.intake_motor.set(speed)

	def outtake(self, speed = .3):
		self.intake_motor.set(-speed)
		self.has_gamepiece = False

	def intake_then_hold_coroutine(self):
		self.has_gamepiece = False
		self.intake(1)
		while True:
			for i in range(20):
				yield
				if self.intake_motor.getSupplyCurrent() < 20:
					break
			else:
				self.intake(0.3)
				self.has_gamepiece = True
				self.robot.leds.set_mode(self.robot.leds.MODE_CARRYING)

	def hatch_down(self):
		self.target_angle = 0

	def hatch_up(self):
		self.target_angle = 90

	def get_rotation(self):
		# 90 degrees is 0.3942
		# 0 degrees is 0.1483
		# return (
		# 	90 # degrees
		# 	/ (.3942-.1483)
		# 	) * (self.encoder.getAbsolutePosition() - 0.1483)
		pass

	def periodic(self):
		self.pid_controller.setGoal(self.target_angle)
		# output = self.pid_controller.calculate(self.get_rotation())
		# self.hatch_motor.set(output)

	def log(self):
		pass