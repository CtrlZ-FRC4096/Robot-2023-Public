import typing

from wpilib import TimedRobot

# from typing import TypeAlias
from .coroutine_command import ensure_generator_function

seconds = float


class CoroutineRobot(TimedRobot):
    _teleop_coro: typing.Generator
    _autonomous_coro: typing.Generator
    _disabled_coro: typing.Generator
    _test_coro: typing.Generator
    _robot_coro: typing.Generator

    def __init__(self, period: seconds = 0.02) -> None:
        super().__init__(period)

        def teleopInit():
            self._teleop_coro = ensure_generator_function(self.teleop_mode)()
            self._autonomous_coro, self._disabled_coro, self._test_coro = None, None, None # type: ignore
            self.teleopPeriodic()

        def teleopPeriodic():
            next(self._teleop_coro, None)

        self.teleopInit = teleopInit
        self.teleopPeriodic = teleopPeriodic

        def autonomousInit():
            self._autonomous_coro = ensure_generator_function(self.autonomous_mode)()
            self._teleop_coro, self._disabled_coro, self._test_coro = None, None, None # type: ignore
            self.autonomousPeriodic()

        def autonomousPeriodic():
            next(self._autonomous_coro, None)

        self.autonomousInit = autonomousInit
        self.autonomousPeriodic = autonomousPeriodic

        def disabledInit():
            self._disabled_coro = ensure_generator_function(self.disabled_mode)()
            self._teleop_coro, self._autonomous_coro, self._test_coro = None, None, None # type: ignore
            self.disabledPeriodic()

        def disabledPeriodic():
            next(self._disabled_coro, None)

        self.disabledInit = disabledInit
        self.disabledPeriodic = disabledPeriodic

        def testInit():
            self._test_coro = ensure_generator_function(self.test_mode)()
            self._teleop_coro, self._autonomous_coro, self._disabled_coro = None, None, None # type: ignore
            self.testPeriodic()

        def testPeriodic():
            next(self._test_coro, None)

        self.testInit = testInit
        self.testPeriodic = testPeriodic

        def robotInit():
            self._robot_coro = ensure_generator_function(self.robot_start)()
            self.robotPeriodic()

        def robotPeriodic():
            next(self._robot_coro, None)

        self.robotInit = robotInit
        self.robotPeriodic = robotPeriodic

    def addPeriodic(self, period: seconds, offset: seconds = 0) -> typing.Callable[[typing.Callable[[], None]], None]:
        def wrapper(callback: typing.Callable[[], None]):
            TimedRobot.addPeriodic(self, callback, period, offset)
        return wrapper

    def robot_start(self):
        """
        Robot-wide code should go here.

        This coroutine is resumed every loop (50 times / second by default)
        """

    def teleop_mode(self):
        """
        Teleop mode code should go here.

        If the robot is in teleop mode, This coroutine is resumed every loop (50 times / second by default)
        If the robot exits teleop mode, this coroutine is cancelled and will start from the beginning the next time the robot enters teleop mode.
        """

    def autonomous_mode(self):
        """
        Autonomous mode code should go here.

        If the robot is in Autonomous mode, This coroutine is resumed every loop (50 times / second by default)
        If the robot exits Autonomous mode, this coroutine is cancelled and will start from the beginning the next time the robot enters Autonomous mode.
        """

    def disabled_mode(self):
        """
        Disabled mode code should go here.

        If the robot is in Disabled mode, This coroutine is resumed every loop (50 times / second by default)
        If the robot exits Disabled mode, this coroutine is cancelled and will start from the beginning the next time the robot enters Disabled mode.
        """

    def test_mode(self):
        """
        Test mode code should go here.

        If the robot is in Test mode, This coroutine is resumed every loop (50 times / second by default)
        If the robot exits Test mode, this coroutine is cancelled and will start from the beginning the next time the robot enters Test mode.
        """
