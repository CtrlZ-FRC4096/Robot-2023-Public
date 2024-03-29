"""
Ctrl-Z FRC Team 4096
FIRST Robotics Competition 2022
Code for robot "swerve drivetrain prototype"
contact@team4096.org

Some code adapted from:
https://github.com/SwerveDriveSpecialties

Some code adapted from:
https://github.com/SwerveDriveSpecialties
"""

"""
Prepend these to any port IDs.
DIO = Digital I/O
AIN = Analog Input
PWM = Pulse Width Modulation
CAN = Controller Area Network
PCM = Pneumatic Control Module
PDP = Power Distribution Panel
"""

import math

from wpimath.geometry import Rotation2d, Translation2d
from wpimath.kinematics import SwerveDrive4Kinematics


### CONSTANTS ###

# Is running simulator. Value is set in robot.py, robotInit
IS_SIMULATION = False

# Directions, mainly used for swerve module positions on drivetrain
FRONT_LEFT = "front_left"
FRONT_RIGHT = "front_right"
BACK_LEFT = "back_left"
BACK_RIGHT = "back_right"

# Robot drivebase dimensions, in inches and meters
DRIVE_BASE_WIDTH = 19.25
DRIVE_BASE_LENGTH = 25
DRIVETRAIN_TRACKWIDTH_METERS = 0.489
DRIVETRAIN_WHEELBASE_METERS = 0.635

SWERVE_MAX_SPEED = 6


# Module PID Constants

# Old values from 2022 Swerve X modules
# SWERVE_ANGLE_KP = 0.43
# SWERVE_ANGLE_KI = 0
# SWERVE_ANGLE_KD = 0.004
# SWERVE_ANGLE_KF = 0

# Values from swerve-test bot MK4 modules
# SWERVE_ANGLE_KP = 0.232
# SWERVE_ANGLE_KI = 0.0625
# SWERVE_ANGLE_KD = 0
# SWERVE_ANGLE_KF = 0

SWERVE_ANGLE_KP = 0.2
SWERVE_ANGLE_KI = 0
SWERVE_ANGLE_KD = .01
SWERVE_ANGLE_KF = 0

SWERVE_DRIVE_KP = .4
SWERVE_DRIVE_KI = 0
SWERVE_DRIVE_KD = .01
SWERVE_DRIVE_KF = 0

SWERVE_DRIVE_KS = 0.02
SWERVE_DRIVE_KV = 1 / 5
SWERVE_DRIVE_KA = 0

# Module Front Left

SWERVE_ANGLE_OFFSET_FRONT_LEFT = Rotation2d.fromDegrees(53.98)  # 234.4
SWERVE_DRIVE_MOTOR_ID_FRONT_LEFT = 18
SWERVE_ANGLE_MOTOR_ID_FRONT_LEFT = 17
SWERVE_CANCODER_ID_FRONT_LEFT = 27  # 8


# Module Front Right

SWERVE_ANGLE_OFFSET_FRONT_RIGHT = Rotation2d.fromDegrees(149.66)  # 235.37
SWERVE_DRIVE_MOTOR_ID_FRONT_RIGHT = 4
SWERVE_ANGLE_MOTOR_ID_FRONT_RIGHT = 5
SWERVE_CANCODER_ID_FRONT_RIGHT = 26  # 5

# Module Back Left
SWERVE_ANGLE_OFFSET_BACK_LEFT = Rotation2d.fromDegrees(122.12)  # 339.96
SWERVE_DRIVE_MOTOR_ID_BACK_LEFT = 15
SWERVE_ANGLE_MOTOR_ID_BACK_LEFT = 16
SWERVE_CANCODER_ID_BACK_LEFT = 25  # 11

# Module Back Right

SWERVE_ANGLE_OFFSET_BACK_RIGHT = Rotation2d.fromDegrees(62.1)  # 5.80
SWERVE_DRIVE_MOTOR_ID_BACK_RIGHT = 2
SWERVE_ANGLE_MOTOR_ID_BACK_RIGHT = 44
SWERVE_CANCODER_ID_BACK_RIGHT = 28  # 2

# Other

SWERVE_WHEEL_CIRCUMFERENCE = math.pi * (4 * 2.54 / 100) # C = pi*d
SWERVE_DRIVE_GEAR_RATIO = 6.55  # From belt kit we ordered
SWERVE_ANGLE_GEAR_RATIO = 10.29  # From Swerve X user guide, for flipped, belt models

SWERVE_DRIVE_MOTOR_INVERTED = True
SWERVE_ANGLE_MOTOR_INVERTED = True

SWERVE_KINEMATICS = SwerveDrive4Kinematics(
    Translation2d(DRIVETRAIN_WHEELBASE_METERS/2.0, DRIVETRAIN_TRACKWIDTH_METERS/2.0),
    Translation2d(DRIVETRAIN_WHEELBASE_METERS/2.0, -DRIVETRAIN_TRACKWIDTH_METERS/2.0),
    Translation2d(-DRIVETRAIN_WHEELBASE_METERS/2.0, DRIVETRAIN_TRACKWIDTH_METERS/2.0),
    Translation2d(-DRIVETRAIN_WHEELBASE_METERS/2.0, -DRIVETRAIN_TRACKWIDTH_METERS/2.0),
)

SWERVE_PIGEON_ID = 0  # 12

SWERVE_INVERT_GYRO = False
SWERVE_INVERT_CANCODERS = False

CAN_PDH = 13

# Auto
AUTO_RESOLUTION = 0.02  # path resolution in seconds
MAX_VEL_METERS_AUTO = 4  # This is the max velocity you want the robot to drive at, not its true max velocity
MAX_ANG_VEL_RAD_AUTO = MAX_VEL_METERS_AUTO / math.hypot(
    DRIVETRAIN_TRACKWIDTH_METERS / 2.0, DRIVETRAIN_WHEELBASE_METERS / 2.0
)  # This is the max velocity you want the robot to rotate at, not its true max rotational velocity
MAX_ACCEL_AUTO = 3  # This is the max rate you want the robot to accelerate at, not its true max acceleration
MAX_ANG_ACCEL_AUTO = (
    6 * math.pi
)  # This is the max rate you want the robot to accelerate at, not its true max acceleration
X_KP = 6 #5  # 0.12667925	#0.73225
X_KI = 0.0 #0.015  # 0.015 #0.0346173		#0.2001
X_KD = 0.01  # 0.01165449	#0.067367
Y_KP = X_KP
Y_KI = X_KI
Y_KD = X_KD
THETA_KP = 5#1.9 #0.232  # * 2.866 * 5.0
THETA_KI = 0.07#0.0625  # * 2.866 * 5.0
THETA_KD = 0.0


JENNY = 8675_309
