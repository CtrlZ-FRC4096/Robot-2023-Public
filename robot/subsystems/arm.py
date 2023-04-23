"""
Ctrl-Z FRC Team 4096
FIRST Robotics Competition 2020
Code for robot "------"
contact@team4096.org
"""
import numpy
import math

# This is to help vscode
from typing import TYPE_CHECKING
if TYPE_CHECKING:
	from robot import Robot

import ctre
import wpilib
import wpimath.controller
from wpimath.trajectory import TrapezoidProfile
from commands2 import Subsystem

class Nodes:
	BK = 0;	NT = 1;	SM = 2;	SH = 3;	FS = 4;	GN = 5; IN = 6
	lookup_table = [
		[BK,NT,NT,NT,NT,NT,NT],
		[BK,NT,SM,IN,SM,GN,IN],
		[BK,NT,SM,SH,FS,GN,IN],
		[IN,IN,SM,SH,FS,SM,IN],
		[BK,NT,SM,SH,FS,SM,IN],
		[BK,NT,SM,SH,FS,GN,IN],
		[BK,NT,SM,SH,FS,GN,IN]
	]

	@classmethod
	def path(cls, curr: int, target: int) -> list[int]:
		next_node = cls.lookup_table[curr][target]
		if next_node == target:
			return [target, curr]
		else:
			return cls.path(next_node,target)+[curr]

class Arm(Subsystem):

	class SETPOINTS:
		SCORE_HIGH = (24,46)
		SCORE_MID = (4.5,42)
		FEEDER_STATION = (16,34)
		NEUTRAL = (0,95)
		BACK = (0, 180) # Over battery
		GROUND_CONE = (0,-10)
		GROUND_CUBE = (0,0) # Not tested
		INTERMEDIATE = (9,50)

		SETPOINTS: list[tuple[float, float]] = [
			BACK,
			NEUTRAL,
			SCORE_MID,
			SCORE_HIGH,
			FEEDER_STATION,
			GROUND_CONE,
			INTERMEDIATE
		]

		@classmethod
		def index(cls, polar: tuple[float, float]):
			return cls.SETPOINTS.index(polar)

	def __init__(self, robot: "Robot"):
		super().__init__()
		self.robot = robot # type: ignore
		self.pivot_motor = ctre.WPI_TalonFX(50)
		self.pivot_motor_2 = ctre.WPI_TalonFX(19)
		self.pivot_encoder = wpilib.DutyCycleEncoder(2)
		self.extension_motor = ctre.WPI_TalonFX(33)
		self.extension_motor.configSupplyCurrentLimit(ctre.SupplyCurrentLimitConfiguration(enable=True,currentLimit=60,triggerThresholdCurrent=0,triggerThresholdTime=0))
		self.gyro_balance = False # Whether or not arm compensates for roll (going onto the ramp)
		self.lower_upper_bound = False # Lower max upper bound from 18 to 4
		# self.pivot_motor.enableVoltageCompensation(True)
		# self.extension_motor.enableVoltageCompensation(True)

		self.extension_motor.config_kP(0,0.2,0)
		self.extension_motor.config_kI(0,0,0)
		self.extension_motor.config_kD(0,0.03,0)
		self.extension_motor.config_kF(0,0,0)
		self.extension_motor.selectProfileSlot(0,0)

		self.extension_motor.configMotionCruiseVelocity(4000000)
		self.extension_motor.configMotionAcceleration(70000)

		inverted = True
		self.pivot_motor.setInverted(inverted)
		self.pivot_motor_2.setInverted(inverted)

		self.pivot_motor_2.follow(self.pivot_motor)

		self.pivot_pid_controller = wpimath.controller.ProfiledPIDController(
			Kp=0.32, Ki=0, Kd=0, constraints = TrapezoidProfile.Constraints(100000,3000)
		)
		self.pivot_feedforward = wpimath.controller.ArmFeedforward(
			kS=0.004*12, kG=0.065*12, kV=0, kA=0
		)

		# self.extension_pid_controller = wpimath.controller.ProfiledPIDController(
		# 	#Kp=1.5, Ki=0, Kd=0, constraints = TrapezoidProfile.Constraints(150,125) # Constraints and PID values are currently arbitrary
		# 	Kp=1.5, Ki=0, Kd=0.03, constraints = TrapezoidProfile.Constraints(1200,500) # Constraints and PID values are currently arbitrary
		# )

		self.pivot_pid_controller.setTolerance(3) # type: ignore

		# Range of length starts at minimum length of arm at 0 inches, maximum limit is 27 inches
		# self.target_angle = self.get_rotation() # Using self.get_rotation() returns around -60 when first called for some reason

		self.target_length = 0
		self.target_angle = 180

		self.target_node = self.SETPOINTS.BACK
		self.path = Nodes.path(0,0)

	inches = float
	degrees = float

	@property
	def target_setpoint(self) -> tuple[inches, degrees]:
		return self.target_node

	@target_setpoint.setter
	def target_setpoint(self, polar: tuple[inches, degrees]):
		curr = self.SETPOINTS.index(self.target_setpoint)
		self.target_node = polar
		target = self.SETPOINTS.index(self.target_setpoint)
		self.path = Nodes.path(curr,target)
		self.path.pop()
		self.target_length, self.target_angle = self.SETPOINTS.SETPOINTS[self.path[-1]]

	def stop(self):
		self.pivot_motor.set(0)
		self.extension_motor.set(0)

	def update_while_disabled(self):
		self.target_angle = self.get_rotation()
		self.target_length = self.get_extension()

	def get_extension(self):
		return (
			16 # inches
			/ 23396 # motor ticks
				) * self.extension_motor.getSelectedSensorPosition()

	def get_rotation(self):
		# 90 degrees is 0.3942
		# 0 degrees is 0.1483
		return (
			90 # degrees
			/ (.3942-.1483)
			) * (self.pivot_encoder.getAbsolutePosition() - 0.1483)

	def is_at_target_angle(self):
		return math.isclose(
			self.target_angle,
			self.get_rotation(),
			abs_tol=5
		)

	def is_at_target_length(self):
		return self.is_at_length(self.target_length) # type: ignore

	def is_at_position(self):
		return self.is_at_target_angle() and self.is_at_target_length()

	def is_at_length(self, length: float):
		return math.isclose(self.get_extension(), length, abs_tol=1)

	def max_length(self):
		angle = self.get_rotation()
		rads = numpy.radians(angle)
		extra_length = 29 # length from pivot to end of telescoping sleeve, need to measure
		bound_back = 25 + extra_length
		bound_top = 18 + extra_length
		bound_front = 12 + extra_length
		top = abs(bound_top / numpy.sin(rads))
		if angle < 90:
			return min(top, abs(bound_front / numpy.cos(rads))) - extra_length
		else:
			return min(top,abs(bound_back / numpy.cos(rads))) - extra_length

	@staticmethod
	def interval(val: float, interval: tuple[float, float]):
		return min(interval[1],max(interval[0],val))

	def periodic(self):
		angle: float = self.get_rotation()
		length: float = self.get_extension()

		at_setpoint = (
			self.pivot_pid_controller.atSetpoint() and
			self.is_at_target_length()
		)
		if not at_setpoint or len(self.path) == 0:
			angle,length = self.target_angle,self.target_length
		else:
			self.target_length,self.target_angle = self.SETPOINTS.SETPOINTS[self.path.pop()]

		# Driver 2 Arm Adjustment
		angle += 10*self.robot.oi.driver2.BOTH_TRIGGERS()

		# Gyro Balance
		if self.gyro_balance:
			angle += self.robot.drivetrain.roll

		# Assures us that the arm will never try to move out of very basic limitations
		self.target_length = self.interval(self.target_length,(0.5,25)) # type: ignore
		angle = self.interval(angle,(-15,180))

		self.pivot_pid_controller.setGoal(angle)
		angle_pid_output = self.pivot_pid_controller.calculate(self.get_rotation())
		angle_ff_output = self.pivot_feedforward.calculate(math.radians(self.get_rotation()),0)
		angle_output = angle_pid_output + angle_ff_output
		wpilib.SmartDashboard.putNumber("Arm/Pivot PID", angle_output)
		self.pivot_motor.setVoltage(angle_output)

		# extension_pid_output = self.extension_pid_controller.calculate(self.get_extension(), length)
		# # extension_pid_output = self.extension_pid_controller.calculate(self.get_extension(), self.target_length)
		# # if not (-0.5 < extension_pid_output < 0.5):
		# # 	extension_pid_output += math.copysign( 0.075*12, extension_pid_output)
		# wpilib.SmartDashboard.putNumber("Arm/Extension PID", extension_pid_output)
		#print(extension_pid_output, extension_pid_output2)
		# self.extension_motor.setVoltage(extension_pid_output)
		self.extension_motor.set(ctre.ControlMode.MotionMagic,length*1462.25)

	def log(self):
		wpilib.SmartDashboard.putNumber("Arm/Pivot Angle", self.get_rotation())
		wpilib.SmartDashboard.putNumber("Arm/Pivot Target Angle", self.target_angle)
		wpilib.SmartDashboard.putNumber("Arm/Extension", self.get_extension())
		wpilib.SmartDashboard.putNumber("Arm/Target Extension", self.target_length)
