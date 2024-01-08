# This is to help vscode
from typing import TYPE_CHECKING
if TYPE_CHECKING:
	from robot import Robot

import math
from limelight import Limelight

from wpimath.trajectory import TrapezoidProfile
from wpilibextra.coroutine.coroutine_command import commandify
from wpilib import Timer
import wpimath.geometry
import const
from commands import autonomous
from commands2 import CommandBase, ParallelCommandGroup, ParallelRaceGroup, SequentialCommandGroup

def _wait(time):
	timer = Timer()
	timer.start()
	while not timer.hasElapsed(time):
		yield

def _stationary_spin(robot: "Robot", rotation: float, abs_tol: float = 2):
	first_time = True
	while not abs(robot.drivetrain.angle_pid.getPositionError()) < abs_tol or first_time:
		yield
		first_time = False
		robot.drivetrain.drive_with_pid(
			wpimath.geometry.Translation2d(0, 0),
			rotation
		)

# @commandify
# def two_piece(robot: "Robot"):
# 	yield from score_high(robot)
# 	yield from _wait(0.5)
# 	robot.arm.target_setpoint = robot.arm.SETPOINTS.NEUTRAL
# 	run_path(robot)

@commandify
def run_path(robot: "Robot"):
	print("Path ------------------------------------------------")
	trajectory = autonomous.DriveTrajectory(robot, "Auto", 4, 3, False)
	trajectory.execute()
	print("Path Done -------------------------------------------")
	#yield from _wait(0.1)
	# robot.drivetrain.stop()

@commandify # men
def run_parallel_path_group(robot: "Robot"):
	print("Path starting")
	trajectory = autonomous.DriveTrajectory(robot, "Auto", 4, 3, False)
	robot.arm.target_setpoint = robot.arm.SETPOINTS.NEUTRAL
	timer = Timer()
	timer.start()
	while not (trajectory.isFinished()):
		trajectory.execute()
		while (timer.hasElapsed(2)) and not (timer.hasElapsed(2.75)):
			robot.intake_side.hatch_down()
			robot.intake_side.intake()
			yield
        # robot.intake_side.periodic()
		yield
	trajectory.end
	robot.intake_side.hatch_up()
@commandify
def run_2_piece_auto_path(robot: "Robot"):
	print("Starting Path")
	trajectory = autonomous.DriveTrajectory(robot, "2 Piece (McNugget)", 4, 3, False)
	robot.arm.target_setpoint = robot.arm.SETPOINTS.NEUTRAL
	timer = Timer()
	timer.start()
	while not (trajectory.isFinished()):
		trajectory.execute()
		while (timer.hasElapsed(1.5)) and not (timer.hasElapsed(2.5)):
			robot.intake_side.hatch_down()
			robot.intake_side.intake()
			yield
		yield
	trajectory.end
	robot.intake_side.hatch_up()

@commandify	
def run_3_piece_auto_path(robot: "Robot"): 
	yield from score_high(robot)
	print("Starting Path")
	trajectory = autonomous.DriveTrajectory(robot, "2 Piece (McNugget)", 1, 1, False)
	robot.arm.target_setpoint = robot.arm.SETPOINTS.NEUTRAL
	timer = Timer()
	timer.start()
	while not (trajectory.isFinished()):
		trajectory.execute()
		while (timer.hasElapsed(1.5)) and not (timer.hasElapsed(2.5)):
			robot.intake_side.hatch_down()
			robot.intake_side.intake()
			yield
		robot.intake_side.hatch_up()
		while (timer.hasElapsed(4)) and not (timer.hasElapsed(5)):
			robot.intake_side.hatch_down()
			robot.intake_side.intake()
			yield
		yield
	trajectory.end
	robot.intake_side.hatch_up()
	#something = trajectory.execute()
	#intaking_method = robot.intake_side.intake_then_hold_coroutine()
	#trajectory.execute()
	#drive_and_set = ParallelCommandGroup(trajectory, hatch_intake, intake_go_down)
	# robot.intake_side.hatch_up()
	# timer = Timer()
	# timer.start()
	# while not (timer.hasElapsed(1)):
	# 	robot.intake_side.periodic()
	# 	yield
	# timer.reset()

	print('Path Done ------------------------------')
	# first_loop = True
	# while not (trajectory.isFinished()):
	# 	if first_loop:
	# 		drive_and_set.execute()
	# 		first_loop = False
	# 	yield from robot.side_intake.periodic()
	# 	print("in loop")
	# 	robot.intake_side.hatch_down()
	# robot.intake_side.hatch_up()
	
	
	


@commandify # Last checked 4/14/23, Status: Good
def score_high(robot: "Robot"):
	robot.drivetrain.set_yaw(180)
	robot.intake.intake(1)
	robot.arm.target_angle = 46
	robot.arm.target_length = 24
	while not robot.arm.is_at_position():
		yield
	robot.arm.target_node = robot.arm.SETPOINTS.SCORE_HIGH
	robot.intake.intake(0.3)
	robot.arm.target_angle -= 10
	yield from _wait(0.5)
	robot.intake.outtake(0.35)
	robot.arm.target_length -= 2
	yield from _wait(0.1)
	robot.arm.target_angle += 10
	yield from _wait(0.5)
	robot.intake.intake(0)
	robot.arm.target_setpoint = robot.arm.SETPOINTS.NEUTRAL

@commandify # Last checked 4/14/23, Status: Good, need to fix bug when delaying after initial mount
def balance(robot: "Robot",towards_front,facing_front):
	yield from robot.drivetrain.balance_coroutine(towards_front=towards_front, facing_front=facing_front)

@commandify # Last checked 4/14/23, Status: Good
def go_all_the_way_over(robot: "Robot", towards_front, rotation, timeout = 0.1):
	speed = 2
	def roll():
		roll = robot.drivetrain.roll
		if rotation == 0:
			roll = -roll
		return roll
	while True:
		yield
		robot.drivetrain.drive_with_pid(
			wpimath.geometry.Translation2d(speed if towards_front else -speed, 0),
			rotation
		)
		if towards_front:
			if roll() < -5:
				break
		else:
			if roll() > 5:
				break
	while not math.isclose(roll(),0,abs_tol=2):
		yield
		robot.drivetrain.drive_with_pid(
			wpimath.geometry.Translation2d(speed if towards_front else -speed, 0),
			rotation
		)
	yield from _wait(timeout)
	robot.drivetrain.stop()

@commandify # Last checked 4/13/23, Status: Good
def go_over(robot: "Robot", towards_front, rotation):
	if rotation == 0:
		robot.arm.target_length = 1
		robot.arm.target_angle = 90
	def roll():
		roll = robot.drivetrain.roll
		if rotation == 0:
			roll = -roll
		return roll
	while True:
		yield
		robot.drivetrain.drive_with_pid(
			wpimath.geometry.Translation2d(4 if towards_front else -4, 0),
			rotation
		)
		if towards_front:
			if roll() < -5:
				break
		else:
			if roll() > 5:
				break
	yield from _stationary_spin(robot, 0)

@commandify # Last checked 4/13/23, Status: Good
def grab_cone(robot: "Robot", polar = (8, -9)):
	robot.limelight.set_to_detector()
	# robot.arm.target_angle = 5
	# robot.arm.target_length = 1
	timeout_timer = Timer()
	timeout_timer.start()
	while (angle_to_cone:=robot.limelight.angle_to_nearest_cone) == None:
		if timeout_timer.hasElapsed(4):		
			robot.arm.gyro_balance = False
			return # End early?
		yield
	angle_to_cone = robot.drivetrain.get_yaw().degrees() - angle_to_cone - 5 # type: ignore
	robot.arm.gyro_balance = True
	yield from _stationary_spin(robot,angle_to_cone)
	robot.drivetrain.stop()
	robot.arm.target_angle = polar[1]
	robot.arm.target_length = polar[0]
	robot.intake.intake(1)
	yield from _wait(1)
	intaking = robot.intake.intake_then_hold_coroutine()
	robot.intake.has_gamepiece = False
	timer = Timer()
	timer.start()
	while not robot.intake.has_gamepiece and not timer.hasElapsed(1.2):
		yield
		x = 2*math.cos(math.radians(angle_to_cone))
		y = 2*math.sin(math.radians(angle_to_cone))
		robot.drivetrain.drive_with_pid(
			wpimath.geometry.Translation2d(x, y),
			angle_to_cone
		)
		print("Moving...")
		next(intaking)
	robot.drivetrain.stop()
	robot.intake.intake(0.3)
	robot.arm.target_angle = 95
	robot.arm.target_length = 0
	yield from _wait(0.5)
	robot.arm.gyro_balance = False

@commandify # Last checked 4/14/23, Status: Good
def score_high_and_balance(robot: "Robot"):
	yield from score_high(robot)
	yield from balance(robot,towards_front=True,facing_front=False)

@commandify # Last checked 4/16/23, Status: Inconsistent, need to check distance from charge station to cone
def score_high_go_all_the_way_over_and_balance(robot: "Robot"):
	yield from score_high(robot)
	yield from _wait(1)
	yield from go_all_the_way_over(robot,True,180,timeout=0.15)
	yield from _wait(0.8)
	yield from balance(robot,towards_front=False,facing_front=False)

@commandify # Last checked 4/16/23, Status: Inconsistent, need to check distance from charge station to cone
def RED_score_high_go_all_the_way_over_and_balance(robot: "Robot"):
	yield from score_high(robot)
	yield from _wait(1)
	yield from go_all_the_way_over(robot,True,180,timeout=0.15)
	timer = Timer()
	timer.start()
	while not timer.hasElapsed(0.2):
		robot.drivetrain.drive_with_pid(
			wpimath.geometry.Translation2d(0, -2), # FLIP? RIGHT
			180
		)
		yield
	yield from _wait(0.8)
	yield from balance(robot,towards_front=False,facing_front=False)

@commandify # Last checked 4/16/23, Status: Inconsistent, need to check distance from charge station to cone
def BLUE_score_high_go_all_the_way_over_and_balance(robot: "Robot"):
	yield from score_high(robot)
	yield from _wait(1)
	yield from go_all_the_way_over(robot,True,180,timeout=0.15)
	timer = Timer()
	timer.start()
	while not timer.hasElapsed(0.2):
		robot.drivetrain.drive_with_pid(
			wpimath.geometry.Translation2d(0, 2), # FLIP? LEFT
			180
		)
		yield
	yield from _wait(0.8)
	yield from balance(robot,towards_front=False,facing_front=False)


@commandify # Last checked 4/16/23, Status: Inconsistent
def score_high_go_all_the_way_over_grab_cone(robot: "Robot"):
	robot.limelight.set_to_detector()
	yield from score_high(robot)
	robot.drivetrain.drive(
		wpimath.geometry.Translation2d(3,0),
		0,
		True,
		True
	)
	yield from _wait(0.2)
	yield from _stationary_spin(robot,0)
	yield from go_all_the_way_over(robot,towards_front=True,rotation=0,timeout=0)
	yield from _wait(0.3)
	yield from grab_cone(robot)

@commandify # Last checked 4/13/23, Status: Inconsistent; see above
def score_high_go_all_the_way_over_grab_cone_balance(robot: "Robot"):
	robot.limelight.set_to_detector()
	yield from score_high(robot)
	robot.drivetrain.drive(
		wpimath.geometry.Translation2d(3,0),
		0,
		True,
		True
	)
	yield from _wait(0.2)
	yield from _stationary_spin(robot,0)
	yield from go_all_the_way_over(robot,towards_front=True,rotation=0,timeout=0.1)
	yield from _wait(0.3)
	yield from grab_cone(robot, polar = (4, -9))
	yield from _wait(0.5)
	yield from _stationary_spin(robot,0)
	yield from balance(robot,towards_front=False,facing_front=True)

@commandify # Last checked 4/13/23, Status: Good
def score_high_side_drive_grab_cone(robot: "Robot"):
	robot.limelight.set_to_detector()
	yield from score_high(robot)
	timer = Timer()
	timer.start()
	robot.drivetrain.drive(
		wpimath.geometry.Translation2d(1.5,0),
		0,
		True,
		True
	)
	yield from _wait(0.6)
	yield from _stationary_spin(robot,0)
	timer.reset()
	while not timer.hasElapsed(1.4):
		yield
		robot.drivetrain.drive_with_pid(
			wpimath.geometry.Translation2d(3,0),
			0
		)
	robot.drivetrain.stop()
	yield from grab_cone(robot)

@commandify # Last checked 4/14/23, Status: Good
def go_all_the_way_over_and_balance(robot: "Robot"):
	yield from go_all_the_way_over(robot,True,0)
	yield from _wait(2)
	yield from balance(robot,towards_front=False,facing_front=True)

@commandify # Incomplete
def place_cone_lower(robot: "Robot"):
	robot.limelight.set_to_retroreflective()
	robot.intake.intake(0.3)
	while (lowest:=robot.limelight.lower_pole) == None:
		yield
	dist, angle = lowest
	angle = robot.drivetrain.get_yaw().degrees() - angle # type: ignore
	# robot.arm.target_angle = 40
	# robot.arm.target_length = 5
	yield from _stationary_spin(robot,angle)
	robot.drivetrain.stop()
	# while dist > 40:
	# 	if (new := robot.limelight.lower_pole) is not None:
	# 		dist, angle = new
	# 		angle += 180
	# 	x = 1*math.cos(math.radians(angle))
	# 	y = 1*math.sin(math.radians(angle))
	# 	robot.drivetrain.drive_with_pid(
	# 		wpimath.geometry.Translation2d(x, y),
	# 		angle
	# 	)
	# 	yield
	# robot.drivetrain.stop()
	# robot.arm.target_angle -= 10
	# yield from _wait(0.5)
	# robot.arm.target_length -= 3
	# robot.intake.outtake(0.3)
	# robot.arm.target_angle += 10
	# yield from _wait(0.5)
	# robot.arm.target_angle = 118
	# robot.arm.target_length = 0

@commandify # Not an auto
def side_to_balance(robot: "Robot",right_side: bool):
	while abs(robot.drivetrain.roll) < 5:
		robot.drivetrain.drive_with_pid(
			wpimath.geometry.Translation2d(-2, 2.5 if right_side else -2.5),
			0
		)
		yield
	robot.drivetrain.stop()

@commandify # Last checked 4/13/23, Status: Good
def right_side_score_high_side_drive_grab_cone_and_balance(robot: "Robot"):
	yield from score_high_side_drive_grab_cone(robot)
	yield from side_to_balance(robot, True)
	yield from balance(robot, towards_front=False, facing_front=True)

@commandify # Last checked 4/15/23, Status: Good
def left_side_score_high_side_drive_grab_cone_and_balance(robot: "Robot"):
	yield from score_high_side_drive_grab_cone(robot)
	yield from side_to_balance(robot, False)
	yield from balance(robot, towards_front=False, facing_front=True)

@commandify # Last checked 4/13/23, Status: Good
def yeet(robot: "Robot"):
	robot.arm.gyro_balance = True
	robot.arm.pivot_pid_controller.setConstraints(TrapezoidProfile.Constraints(100000,1000000))
	robot.intake.intake(0.3)
	robot.arm.target_angle = 45
	robot.arm.target_length = 12
	while not robot.arm.get_rotation() < 130:
		yield
	robot.intake.outtake(1)
	yield from _wait(0.5)
	robot.intake.stop()
	robot.arm.pivot_pid_controller.setConstraints(TrapezoidProfile.Constraints(100000,3000))
	robot.arm.target_angle = 118
	robot.arm.target_length = 0
	robot.arm.gyro_balance = False

@commandify # Just doesn't do anything
def no_auto(robot: "Robot"):
	yield

@commandify # Last checked 4/14/23, Status: Good
def score_high_side_drive_grab_cone_yeet(robot: "Robot"):
	robot.limelight.set_to_detector()
	yield from score_high_side_drive_grab_cone(robot)
	robot.arm.target_length = 0
	robot.arm.target_angle = 95
	yield from _wait(0.5)
	yield from _stationary_spin(robot,173)
	robot.arm.target_angle = 180
	while -robot.drivetrain.roll < 1:
		robot.drivetrain.drive_with_pid(
			wpimath.geometry.Translation2d(-2, 0),
			173 # 0 or 180?
		)
		yield
	robot.drivetrain.stop()
	yield from _wait(0.5)
	yield from yeet(robot)

@commandify # Untested
def score_high_side_drive_grab_cone_score_low(robot: "Robot"):
	yield from score_high_side_drive_grab_cone(robot)
	robot.arm.target_setpoint = robot.arm.SETPOINTS.NEUTRAL
	while abs(robot.drivetrain.modules[0].get_state().speed) < 1.6:
		yield
		robot.drivetrain.drive_with_pid(
			wpimath.geometry.Translation2d(-2, 0),
			0
		)
	yield from _wait(0.1)
	while abs(robot.drivetrain.modules[0].get_state().speed) > 1.5:
		yield
		robot.drivetrain.drive_with_pid(
			wpimath.geometry.Translation2d(-2, 0),
			0
		)
	robot.drivetrain.stop()
	robot.intake.outtake(0.3)
	yield from _wait(0.5)
	robot.intake.stop()
	robot.arm.target_setpoint = robot.arm.SETPOINTS.NEUTRAL