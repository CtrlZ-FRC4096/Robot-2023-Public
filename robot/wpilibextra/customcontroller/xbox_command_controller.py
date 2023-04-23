from wpilib import XboxController
from wpilib.interfaces import GenericHID

from . import CustomAnalog

# from commands2.button import Button
from .custom_button import CustomButton as Button


class XboxCommandController:
    """This class provides an easy way to link buttons/analogs/triggers/dpad to commands/functions on an Xbox(360/One) controller.

    It is very easy to link a button to a command.  For instance, you could
    link the trigger button of a joystick to a "score" command.
    You can also create custom buttons using any boolean function.
    You can also control the rumble(vibration) feature of the xbox controller
    """

    def __init__(self, port: int) -> None:
        """Creates an instance of the XboxCommandController class

        :param port: DriverStation port number for the xbox controller
        """
        xbox = self.xbox = XboxController(port)
        self.A = Button(xbox.getAButton)
        self.B = Button(xbox.getBButton)
        self.X = Button(xbox.getXButton)
        self.Y = Button(xbox.getYButton)
        self.LEFT_BUMPER = Button(xbox.getLeftBumper)
        self.RIGHT_BUMPER = Button(xbox.getRightBumper)
        self.START = Button(xbox.getStartButton)
        self.BACK = Button(xbox.getBackButton)
        self.LEFT_STICK = Button(xbox.getLeftStickButton)
        self.RIGHT_STICK = Button(xbox.getRightStickButton)

        self.LEFT_JOY_X = CustomAnalog(xbox.getLeftX)
        self.LEFT_JOY_Y = CustomAnalog(xbox.getLeftY)
        self.RIGHT_JOY_X = CustomAnalog(xbox.getRightX)
        self.RIGHT_JOY_Y = CustomAnalog(xbox.getRightY)
        self.LEFT_TRIGGER = CustomAnalog(xbox.getLeftTriggerAxis)
        self.RIGHT_TRIGGER = CustomAnalog(xbox.getRightTriggerAxis)

        self.POV = POVWrapper(xbox.getPOV)

        self.BOTH_TRIGGERS = CustomAnalog(
            lambda: -(self.LEFT_TRIGGER.getRaw())
            if self.LEFT_TRIGGER.getRaw() > self.RIGHT_TRIGGER.getRaw()
            else self.RIGHT_TRIGGER.getRaw()
        )
        self.LEFT_TRIGGER_AS_BUTTON = Button(lambda: self.LEFT_TRIGGER.getRaw() > 0.05)
        self.RIGHT_TRIGGER_AS_BUTTON = Button(
            lambda: self.RIGHT_TRIGGER.getRaw() > 0.05
        )

        self.LEFT_JOY_UP = Button(lambda: self.LEFT_JOY_Y.getRaw() < -0.1)
        self.LEFT_JOY_DOWN = Button(lambda: self.LEFT_JOY_Y.getRaw() > 0.1)
        self.LEFT_JOY_LEFT = Button(lambda: self.LEFT_JOY_X.getRaw() < -0.1)
        self.LEFT_JOY_RIGHT = Button(lambda: self.LEFT_JOY_X.getRaw() > 0.1)

        self.RIGHT_JOY_UP = Button(lambda: self.RIGHT_JOY_Y.getRaw() < -0.1)
        self.RIGHT_JOY_DOWN = Button(lambda: self.RIGHT_JOY_Y.getRaw() > 0.1)
        self.RIGHT_JOY_LEFT = Button(lambda: self.RIGHT_JOY_X.getRaw() < -0.1)
        self.RIGHT_JOY_RIGHT = Button(lambda: self.RIGHT_JOY_X.getRaw() > 0.1)

    def getController(self):
        """
        :returns: The wpilib XboxController object stored wihtin this class
        """
        return self.xbox

    def setLeftRumble(self, intensity=1):
        """Sets the Rumble(Vibration) for the left side of the controller

        :param intensity: How powerful the vibration should be
        """
        self.xbox.setRumble(GenericHID.RumbleType.kLeftRumble, intensity)

    def setRightRumble(self, intensity=1):
        """Sets the Rumble(Vibration) for the right side of the controller

        :param intensity: How powerful the vibration should be
        """
        self.xbox.setRumble(GenericHID.RumbleType.kRightRumble, intensity)

    def setRumble(self, intensity=1):
        """Sets the Rumble(Vibration) for the entire controller

        :param intensity: How powerful the vibration should be
        """
        self.setLeftRumble(intensity)
        self.setRightRumble(intensity)

    def setRumbleByLocation(self, baseIntensity=0, location=0):
        """Sets the Rumble(Vibration) based on where the vibration should occur

        :param baseIntensity: How powerful the vibration should be in the center [0, 1]
        :param location: Where the vibration should occur [-1, 1] -1 is full left. 1 is full right
        """
        self.setLeftRumble(baseIntensity - location)
        self.setRightRumble(baseIntensity + location)


class POVWrapper:
    def __call__(self):
        """Calls get() on this object.

        :returns: the value of get()
        """
        if self._getPOV == None:
            raise RuntimeError("This Controller was not properly initialized")
        return self.get()

    def __init__(self, getPOV):
        """Creates all CustomButton objects for the POV."""

        self._getPOV = getPOV

        is_pressed = lambda v: getPOV(0) == v

        self.NONE = Button(lambda: is_pressed(-1))
        self.ANY = Button(lambda: self.get() != 0)
        self.UP = Button(lambda: is_pressed(0))
        self.DOWN = Button(lambda: is_pressed(180))
        self.LEFT = Button(lambda: is_pressed(270))
        self.RIGHT = Button(lambda: is_pressed(90))
        self.DIAG_UP_LEFT = Button(lambda: is_pressed(315))
        self.DIAG_UP_RIGHT = Button(lambda: is_pressed(45))
        self.DIAG_DOWN_LEFT = Button(lambda: is_pressed(225))
        self.DIAG_DOWN_RIGHT = Button(lambda: is_pressed(135))

    def get(self):
        """Gets the raw value of the POV

        :returns: raw value of the POV
        """
        return self._getPOV(0)
