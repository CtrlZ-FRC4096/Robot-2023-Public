"""
Ctrl-Z FRC Team 4096
FIRST Robotics Competition 2023
Code for robot "swerve drivetrain prototype"
contact@team4096.org

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

SWERVE_WHEEL_CIRCUMFERENCE = 2 * math.pi * (4 * 2.54 / 100)
SWERVE_DRIVE_GEAR_RATIO = 6.55  # From belt kit we ordered
SWERVE_ANGLE_GEAR_RATIO = 10.29  # From Swerve X user guide, for flipped, belt models

SWERVE_DRIVE_MOTOR_INVERTED = True
SWERVE_ANGLE_MOTOR_INVERTED = True

SWERVE_KINEMATICS = SwerveDrive4Kinematics(
    Translation2d(DRIVETRAIN_WHEELBASE_METERS / 2, DRIVETRAIN_TRACKWIDTH_METERS / 2),
    Translation2d(DRIVETRAIN_WHEELBASE_METERS / 2, -DRIVETRAIN_TRACKWIDTH_METERS / 2),
    Translation2d(-DRIVETRAIN_WHEELBASE_METERS / 2, DRIVETRAIN_TRACKWIDTH_METERS / 2),
    Translation2d(-DRIVETRAIN_WHEELBASE_METERS / 2, -DRIVETRAIN_TRACKWIDTH_METERS / 2),
)

SWERVE_PIGEON_ID = 0  # 12

SWERVE_INVERT_GYRO = False
SWERVE_INVERT_CANCODERS = False

JENNY = 8675_309
