import time
import math
from ctre import Pigeon2, PigeonIMU, TalonSRX
from wpilib import DriverStation, SmartDashboard, Timer
from wpimath.geometry import Pose2d, Rotation2d, Translation2d
from wpimath.kinematics import (
    ChassisSpeeds,
    SwerveDrive4Kinematics,
    SwerveDrive4Odometry,
    SwerveModulePosition,
)

import const

# from commands2 import SubsystemBase
from wpilibextra.coroutine.subsystem import SubsystemBase
from swerve.swervemodule import SwerveModule
from wpimath.controller import PIDController
from wpilibextra.PIDD2Controller import PIDD2Controller

class Drivetrain(SubsystemBase):
	def __init__(self, robot):
		super().__init__()
		self.robot = robot
		# self.gyrotalon = TalonSRX(12)
		# self.gyro = PigeonIMU(self.gyrotalon)
		self.gyro = Pigeon2(const.SWERVE_PIGEON_ID, "carnivore")
		self.gyro.configFactoryDefault()
		self.zero_gyro()
		self.gyro_offset = 0.0
		self.angle_pid = PIDD2Controller(0.16,0,0.003, 0)
		self.angle_pid.enableContinuousInput(0,360)

		self.modules = [
		    SwerveModule(
		        "front_left",
		        const.SWERVE_ANGLE_OFFSET_FRONT_LEFT,
		        const.SWERVE_DRIVE_MOTOR_ID_FRONT_LEFT,
		        const.SWERVE_ANGLE_MOTOR_ID_FRONT_LEFT,
		        const.SWERVE_CANCODER_ID_FRONT_LEFT,
		        ),
		    SwerveModule(
		        "front_right",
		        const.SWERVE_ANGLE_OFFSET_FRONT_RIGHT,
		        const.SWERVE_DRIVE_MOTOR_ID_FRONT_RIGHT,
		        const.SWERVE_ANGLE_MOTOR_ID_FRONT_RIGHT,
		        const.SWERVE_CANCODER_ID_FRONT_RIGHT,
		        ),
		    SwerveModule(
		        "back_left",
		        const.SWERVE_ANGLE_OFFSET_BACK_LEFT,
		        const.SWERVE_DRIVE_MOTOR_ID_BACK_LEFT,
		        const.SWERVE_ANGLE_MOTOR_ID_BACK_LEFT,
		        const.SWERVE_CANCODER_ID_BACK_LEFT,
		        ),
		    SwerveModule(
		        "back_right",
		        const.SWERVE_ANGLE_OFFSET_BACK_RIGHT,
		        const.SWERVE_DRIVE_MOTOR_ID_BACK_RIGHT,
		        const.SWERVE_ANGLE_MOTOR_ID_BACK_RIGHT,
		        const.SWERVE_CANCODER_ID_BACK_RIGHT,
		        ),
		]

		# This is to give CANCoders time to settle. Normally sleep calls are very bad but they're okay
		# here in the constructor/init.
		time.sleep(1.0)
		self.reset_modules_to_absolute()

		self.odometry = SwerveDrive4Odometry(
		    const.SWERVE_KINEMATICS, self.get_yaw(), self.get_module_positions()
		)

	def drive(self, translation: Translation2d, rotation, field_relative, is_open_loop):
		SmartDashboard.putNumber("Swerve/Translation X", translation.x)
		SmartDashboard.putNumber("Swerve/Translation Y", translation.y)
		SmartDashboard.putNumber("Swerve/Rotation", rotation)
		SmartDashboard.putBoolean("Swerve/With PID", False)
		if field_relative:
			module_states = const.SWERVE_KINEMATICS.toSwerveModuleStates(
			    ChassisSpeeds.fromFieldRelativeSpeeds(
			        translation.x,
			        translation.y,
			        rotation,
			        self.get_yaw(),
			    )
			)
		else:
			module_states = const.SWERVE_KINEMATICS.toSwerveModuleStates(
			    ChassisSpeeds(
			        translation.x,
			        translation.y,
			        rotation,
			    )
			)
		SwerveDrive4Kinematics.desaturateWheelSpeeds(
		    module_states, const.SWERVE_MAX_SPEED
		)

		for idx, module in enumerate(self.modules):
			# if module.module_name != 'front_right':
			# 	continue
			module.set_desired_state(module_states[idx], is_open_loop)

	def drive_with_pid(self, translation: Translation2d, target_angle):
		in_motion = not (math.isclose(translation.x,0,abs_tol=0.2) and math.isclose(translation.y,0,abs_tol=0.2))
		if in_motion:
			self.angle_pid.setPID(0.06,0,0,0)
		else:
			self.angle_pid.setPID(0.15,0,0.004, 0)
		pid_output = self.angle_pid.calculate(self.get_yaw().degrees() % 360,target_angle) #type: ignore
		if not in_motion:
			pid_output += math.copysign(0.7,pid_output)
		SmartDashboard.putBoolean("Swerve/With PID", True)
		self.drive(translation,pid_output,True,True)


	def stop(self):
		self.drive(Translation2d(0,0), 0, False, True)

	def set_module_states(self, desired_states):
		SwerveDrive4Kinematics.desaturateWheelSpeeds(
		    desired_states, const.SWERVE_MAX_SPEED
		)

		for idx, module in enumerate(self.modules):
			module.set_desired_state(desired_states[idx], False)

	def get_pose(self):
		return self.odometry.getPose()

	def reset_odometry(self, pose):
		self.odometry.resetPosition(self.get_yaw(), pose, *self.get_module_positions())

	def get_module_states(self):
		return tuple(
		    [
		        # Java returns a copy of the state value. Relevant?
		        module.get_state()
		        for module in self.modules
		    ]
		)

	def get_module_positions(self):
		return tuple([module.get_position() for module in self.modules])

	def zero_gyro(self):
		self.set_yaw(0)

	def set_yaw(self, yaw):
		SmartDashboard.putNumber("Gyro/Set Yaw", yaw)
		self.gyro.setYaw(yaw)

	@property
	def roll(self):
		return self.gyro.getRoll() - self.gyro_offset

	def get_yaw(self):
		if const.SWERVE_INVERT_GYRO:
			return Rotation2d.fromDegrees(360 - self.gyro.getYaw())
		else:
			return Rotation2d.fromDegrees(self.gyro.getYaw())

	def reset_modules_to_absolute(self):
		for module in self.modules:
			module.reset_to_absolute()

	def periodic(self):
		# if DriverStation.isDisabled():
		# 	self.reset_modules_to_absolute()

		self.odometry.update(self.get_yaw(), *self.get_module_positions())

		SmartDashboard.putNumber("Swerve/Odometry X", self.odometry.getPose().x_feet)
		SmartDashboard.putNumber("Swerve/Odometry Y", self.odometry.getPose().y_feet)

		SmartDashboard.putNumber("Gyro/Yaw", self.gyro.getYaw())
		SmartDashboard.putNumber("Gyro/Roll", self.roll)

		for module in self.modules:
			SmartDashboard.putNumber(f"Swerve/{module.module_name}/Cancoder Angle", module.get_angle_CANcoder().degrees())  # type: ignore
			SmartDashboard.putNumber(f"Swerve/{module.module_name}/Motor Angle", module.get_position().angle.degrees())  # type: ignore
			SmartDashboard.putNumber(
			    f"Swerve/{module.module_name}/Velcoity", module.get_state().speed
			)

	def log(self):
		pass

	def balance_coroutine(self, *, towards_front: bool, facing_front: bool):
		self.robot.arm.target_angle = 90
		speed = 5
		def roll():
			roll = self.roll
			if facing_front:
				roll = -roll
			return roll
		def drive_forward(speed):
			self.drive_with_pid(
				Translation2d(speed, 0),
				0 if facing_front else 180
			)
		drive_forward(speed if towards_front else -speed)
		while abs(roll()) < 13:
			drive_forward(speed if towards_front else -speed)
			yield
		timer = Timer()
		timer.start()
		while not timer.hasElapsed(0.5):
			yield
		times_run = 0
		while True:
			max_angle = -1e99
			delta = 0
			while delta < 2 or abs(roll()) > 18:
				yield
				max_angle = max(max_angle, abs(roll()))
				delta = max_angle - abs(roll())
				drive_forward(math.copysign(1,roll()))
				print("Gyro Value: ",roll(),"  Max Angle: ",max_angle,"  Delta ",delta)
			self.stop()

			timer = Timer()
			timer.start()
			times_run += 1
			while not timer.hasElapsed(1) and not times_run == 1:
				print("Holding...")
				yield
			if(abs(roll()) < 5): #  or times_run > 4
				break
		self.stop()