from wpimath.geometry import Rotation2d
from wpimath.kinematics import SwerveModuleState

def optimize(desired_state: SwerveModuleState, current_angle: Rotation2d):
    target_angle = in_0_to_360_scope(
        current_angle.degrees(), desired_state.angle.degrees() # type: ignore
    )
    target_speed: float = desired_state.speed
    delta = target_angle - current_angle.degrees() # type: ignore
    if abs(delta) > 90:
        target_speed = -target_speed
        if delta > 90:
            target_angle = target_angle - 180
        else:
            target_angle = target_angle + 180
    return SwerveModuleState(target_speed, Rotation2d.fromDegrees(target_angle))

def in_0_to_360_scope(scope_reference: float, new_angle: float):
    lower_offset = scope_reference % 360
    if lower_offset >= 0:
        lower_bound = scope_reference - lower_offset
        upper_bound = scope_reference + 360 - lower_offset
    else:
        upper_bound = scope_reference - lower_offset
        lower_bound = scope_reference + 360 - lower_offset
    while new_angle < lower_bound:
        new_angle = new_angle + 360
    while new_angle > upper_bound:
        new_angle = new_angle - 360
    if new_angle - scope_reference > 180:
        new_angle = new_angle - 360
    elif new_angle - scope_reference < -180:
        new_angle = new_angle + 360
    return new_angle
