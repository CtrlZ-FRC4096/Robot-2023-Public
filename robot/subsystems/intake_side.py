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
		self.hatch_motor.setInverted(True)
		self.encoder = wpilib.DutyCycleEncoder(1)
		self.intake_motor = ctre.WPI_TalonFX(42)
		self.intake_motor.setInverted(True)
		self.intake_motor.configSupplyCurrentLimit(ctre.SupplyCurrentLimitConfiguration(enable=True,currentLimit=60,triggerThresholdCurrent=0,triggerThresholdTime=0))
		self.has_gamepiece = False
		self.pid_controller = wpimath.controller.ProfiledPIDController(
			Kp=.01, Ki=0, Kd=0, constraints = TrapezoidProfile.Constraints(10000000,1000000)
		)
		self.target_angle = 98

	def stop(self):
		self.hatch_motor.set(0)
		self.intake_motor.set(0)

	def intake(self, speed = .5):
		speed = abs(speed)
		self.intake_motor.set(speed)

	def outtake(self, speed = .5):
		speed = abs(speed)
		self.intake_motor.set(-speed)
		self.has_gamepiece = False

	def intake_then_hold_coroutine(self):
		if self.has_gamepiece and self.intake_motor.getSupplyCurrent() > 0.5:
			return
		self.has_gamepiece = False
		self.intake(0.5)
		while self.intake_motor.getSupplyCurrent() < 8:
			yield
		while self.intake_motor.getSupplyCurrent() > 8:
			yield
		while True:
			yield
			if self.intake_motor.getSupplyCurrent() > 8:
				self.intake(0.08)
				self.has_gamepiece = True
				self.robot.leds.set_mode(self.robot.leds.MODE_CARRYING)
				break
		yield
		yield
		yield
		yield
		self.hatch_up()

	def hatch_down(self):
		self.target_angle = 0


	def hatch_up(self):
		self.target_angle = 98

	def get_rotation(self):
		# 90 degrees is 0.7258
		# 0 degrees is 0.967
		return (
			90 # degrees
			/ (.967-.7258)
			) * (0.967 - self.encoder.getAbsolutePosition())

	def periodic(self):
		self.pid_controller.setGoal(self.target_angle)
		output = self.pid_controller.calculate(self.get_rotation())

		# Feed forward, function of angle that attempts to cancel

		self.hatch_motor.set(output)

        
	def log(self):
		wpilib.SmartDashboard.putNumber("Side Intake Angle", self.encoder.getAbsolutePosition())
		wpilib.SmartDashboard.putNumber("Side Intake Current", self.intake_motor.getSupplyCurrent())
