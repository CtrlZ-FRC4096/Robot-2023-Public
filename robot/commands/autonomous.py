# This is to help vscode
from typing import TYPE_CHECKING

from wpilib._wpilib import SmartDashboard, wait
from wpimath.controller import PIDController, ProfiledPIDController
from wpimath.geometry._geometry import Pose2d, Rotation2d
from wpimath.kinematics._kinematics import SwerveModuleState
from wpimath.trajectory import TrapezoidProfile

# from pathplannerlib.swerve_path_controller import SwervePathController
# from commands.drive_follow_path import DriveFollowPath

# from robotpy import PathPlanner

if TYPE_CHECKING:
    from robot import Robot

import math

from commands2 import (
    CommandBase,
    ParallelCommandGroup,
    ParallelRaceGroup,
    SequentialCommandGroup,
)
from commands2._impl import CommandBase
from wpilib import Timer
from wpimath import controller, geometry
from wpimath.kinematics import ChassisSpeeds

import const
from wpilibextra.coroutine import CoroutineCommand, commandify

# @commandify
# def Auto1(robot: Robot):
# 	pass

# 	if robot.nt_robot.get
# 	DriveTrajectory()


class DriveTrajectory(CommandBase):
    def __init__(self, robot: "Robot", path, max_vel, max_accel, reversed):
        super().__init__()
        self.robot = robot
        self.path = path
        # self.target = PathPlanner.loadPath(self.path, max_vel, max_accel, reversed)

        self.timer = Timer()

        # rotation = self.target.sample(0).holonomicRotation
        # self.robot.drivetrain.set_gyro(rotation.degrees())
        # self.robot.drivetrain.odometry.resetPosition(self.target.sample(0).pose, rotation)

        self.hcontroller = betterHolonomicDriveController()
        self.timer.start()

    # Overrides
    def getRequirements(self):
        return set([self.robot.drivetrain])

    def execute(self):
        # targetState = self.target.sample(self.timer.get())
        # currentPose = self.robot.drivetrain.getPose2d()
        # self.hcontroller.drive(self.robot, currentPose, targetState)
        ...

    def isFinished(self):
        # finished = self.timer.hasElapsed(self.target.getTotalTime())
        # return finished
        return True

    def end(self, interrupted):
        self.timer.stop()
        # self.robot.drivetrain.defense()
        pass

    def interrupted(self):
        self.end(True)


class betterHolonomicDriveController:
    def __init__(self):
        """
        Creates drive controller
        """
        self.x_controller = controller.PIDController(const.X_KP, const.X_KI, const.X_KD)
        self.y_controller = controller.PIDController(const.Y_KP, const.Y_KI, const.Y_KD)
        self.theta_controller = controller.PIDController(
            const.THETA_KP, const.THETA_KI, const.THETA_KD
        )
        self.x_controller.reset()
        self.y_controller.reset()
        self.theta_controller.reset()

    def calculate(self, currentPose, targetState):
        """
        Calculates chassis speeds
        @parameter (Pose2d) currentPose		Robot's current pose
        @parameter (State) targetState		Robot's target state
        @returns (tuple) (vx, vy, omega)	Robot's left-right, forward-backward, and angular velocities (m/s, m/s, rad/s)
        """
        # calculates the percent outputs in the x, y, and theta directions
        vx = self.x_controller.calculate(currentPose.X(), targetState.pose.X())
        vy = self.y_controller.calculate(currentPose.Y(), targetState.pose.Y())
        # current and target angles must be put into the range [-math.pi, math.pi)
        targetHeading = self.optimize(currentPose, targetState)
        omega = self.theta_controller.calculate(
            currentPose.rotation().radians(), targetHeading
        )

        return (vx, vy, omega)

    def optimize(self, currentPose, targetState):
        """
        .enableContinuousInput() doesn't work so we have this
        @parameter (Pose2d) currentPose		Robot's current pose
        @parameter (State) targetState		Robot's target state
        @returns (double) targetHeading		optimized heading
        """
        currentHeading = currentPose.rotation().radians()

        targetHeading = targetState.holonomicRotation.radians()
        if targetHeading - currentHeading > math.pi:
            targetHeading -= 2 * math.pi
        elif targetHeading - currentHeading < -math.pi:
            targetHeading += 2 * math.pi

        return targetHeading

    def drive(self, robot, currentPose, targetState):
        """
        Calculates chassis speeds and drives the robot
        """
        calcs = self.calculate(currentPose, targetState)
        left_right = calcs[0]
        forward_back = calcs[1]
        omega = calcs[2]
        chassis_speeds = ChassisSpeeds.fromFieldRelativeSpeeds(
            vx=left_right,
            vy=forward_back,
            omega=omega,
            robotAngle=currentPose.rotation(),
        )

        robot.drivetrain.drive(chassis_speeds)
        robot.drivetrain.periodic()
