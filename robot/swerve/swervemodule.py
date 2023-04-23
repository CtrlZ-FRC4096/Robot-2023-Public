import typing

from ctre import (
    AbsoluteSensorRange,
    CANCoder,
    CANCoderConfiguration,
    ControlMode,
    DemandType,
    NeutralMode,
    SensorInitializationStrategy,
    SensorTimeBase,
    SupplyCurrentLimitConfiguration,
    TalonFX,
    TalonFXConfiguration,
)
from wpimath.controller import SimpleMotorFeedforwardMeters
from wpimath.geometry import Rotation2d
from wpimath.kinematics import SwerveModulePosition, SwerveModuleState

import const
from swerve import conversions, ctre_module_state


class SwerveModule:
    module_name: str
    angle_offset: Rotation2d
    last_angle: Rotation2d

    angle_motor: TalonFX
    drive_motor: TalonFX
    angle_encoder: CANCoder

    def __init__(
        self,
        module_name: str,
        angle_offset: Rotation2d,
        drive_motor_id: int,
        angle_motor_id: int,
        cancoder_id: int,
    ):
        self.module_name = module_name
        self.angle_offset = angle_offset

        self.angle_encoder = CANCoder(cancoder_id, "carnivore")
        self.angle_motor = TalonFX(angle_motor_id, "carnivore")
        self.drive_motor = TalonFX(drive_motor_id, "carnivore")

        self.angle_encoder.configFactoryDefault()
        swerve_can_coder_config = CANCoderConfiguration()
        swerve_can_coder_config.absoluteSensorRange = (
            AbsoluteSensorRange.Unsigned_0_to_360
        )
        swerve_can_coder_config.sensorDirection = const.SWERVE_INVERT_CANCODERS
        swerve_can_coder_config.initializationStrategy = (
            SensorInitializationStrategy.BootToAbsolutePosition
        )
        swerve_can_coder_config.sensorTimeBase = SensorTimeBase.PerSecond
        self.angle_encoder.configAllSettings(swerve_can_coder_config)

        self.angle_motor.configFactoryDefault()
        swerve_angle_motor_config = TalonFXConfiguration()
        swerve_angle_motor_config.slot0.kP = const.SWERVE_ANGLE_KP
        swerve_angle_motor_config.slot0.kI = const.SWERVE_ANGLE_KI
        swerve_angle_motor_config.slot0.kD = const.SWERVE_ANGLE_KD
        swerve_angle_motor_config.slot0.kF = const.SWERVE_ANGLE_KF
        swerve_angle_motor_config.supplyCurrLimit = SupplyCurrentLimitConfiguration(
            enable=True,
            currentLimit=25,
            triggerThresholdCurrent=40,
            triggerThresholdTime=0.1,
        )
        self.angle_motor.configAllSettings(swerve_angle_motor_config)
        self.angle_motor.setInverted(const.SWERVE_ANGLE_MOTOR_INVERTED)
        self.angle_motor.setNeutralMode(NeutralMode.Brake)

        self.reset_to_absolute()

        self.drive_motor.configFactoryDefault()
        swerve_drive_motor_config = TalonFXConfiguration()
        swerve_drive_motor_config.slot0.kP = const.SWERVE_DRIVE_KP
        swerve_drive_motor_config.slot0.kI = const.SWERVE_DRIVE_KI
        swerve_drive_motor_config.slot0.kD = const.SWERVE_DRIVE_KD
        swerve_drive_motor_config.slot0.kF = const.SWERVE_DRIVE_KF
        swerve_drive_motor_config.supplyCurrLimit = SupplyCurrentLimitConfiguration(
            enable=True,
            currentLimit=20,
            triggerThresholdCurrent=40,
            triggerThresholdTime=0.1,
        )
        self.drive_motor.configAllSettings(swerve_drive_motor_config)
        self.drive_motor.setInverted(const.SWERVE_DRIVE_MOTOR_INVERTED)
        self.drive_motor.setNeutralMode(NeutralMode.Brake)
        self.drive_motor.setSelectedSensorPosition(0)

        self.last_angle = self.get_state().angle

        self.feedforward = SimpleMotorFeedforwardMeters(
            const.SWERVE_DRIVE_KS, const.SWERVE_DRIVE_KV, const.SWERVE_DRIVE_KA
        )

    def set_desired_state(self, desired_state: SwerveModuleState, is_open_loop):
        desired_state = ctre_module_state.optimize(
            desired_state, self.get_state().angle
        )
        self.set_angle(desired_state)
        self.set_speed(desired_state, is_open_loop)

    def set_speed(self, desired_state: SwerveModuleState, is_open_loop):
        if is_open_loop:
            percent_output = desired_state.speed / const.SWERVE_MAX_SPEED
            self.drive_motor.set(ControlMode.PercentOutput, percent_output)
        else:
            velocity = conversions.MPS_to_falcon(
                desired_state.speed,
                const.SWERVE_WHEEL_CIRCUMFERENCE,
                const.SWERVE_DRIVE_GEAR_RATIO,
            )
            self.drive_motor.set(
                ControlMode.Velocity,
                velocity,
                DemandType.ArbitraryFeedForward,
                self.feedforward.calculate(desired_state.speed),
            )

    def set_angle(self, desired_state: SwerveModuleState):
        if abs(desired_state.speed) <= const.SWERVE_MAX_SPEED * 0.01:
            angle = self.last_angle
        else:
            angle = desired_state.angle

        self.angle_motor.set(
            ControlMode.Position,
            conversions.degrees_to_falcon(
                angle.degrees(), const.SWERVE_ANGLE_GEAR_RATIO
            ),
        )
        self.last_angle = angle

    def get_angle(self):
        # return self.get_angle_CANcoder()
        return Rotation2d.fromDegrees(
            conversions.falcon_to_degrees(
                self.angle_motor.getSelectedSensorPosition(),
                const.SWERVE_ANGLE_GEAR_RATIO,
            )
        )

    def get_angle_CANcoder(self):
        return Rotation2d.fromDegrees(self.angle_encoder.getAbsolutePosition())

    def get_state(self):
        return SwerveModuleState(
            conversions.falcon_to_MPS(
                self.drive_motor.getSelectedSensorVelocity(),
                const.SWERVE_WHEEL_CIRCUMFERENCE,
                const.SWERVE_DRIVE_GEAR_RATIO,
            ),
            self.get_angle(),
        )

    def get_position(self):
        return SwerveModulePosition(
            conversions.falcon_to_meters(
                self.drive_motor.getSelectedSensorPosition(),
                const.SWERVE_WHEEL_CIRCUMFERENCE,
                const.SWERVE_DRIVE_GEAR_RATIO,
            ),
            self.get_angle(),
        )

    def reset_to_absolute(self):
        cancoder_angle: float = typing.cast(float, self.get_angle_CANcoder().degrees())
        angle_offset: float = typing.cast(float, self.angle_offset.degrees())
        absolute_position = conversions.degrees_to_falcon(
            cancoder_angle - angle_offset, const.SWERVE_ANGLE_GEAR_RATIO
        )
        self.angle_motor.setSelectedSensorPosition(absolute_position)
