def CANcoder_to_degrees(position_counts, gear_ratio):
    return position_counts * (360 / (gear_ratio * 4096))


def degrees_to_CANcoder(degrees, gear_ratio):
    return degrees * (360 / (gear_ratio * 4096))


def falcon_to_degrees(position_counts, gear_ratio):
    return position_counts * (360 / (gear_ratio * 2048))


def degrees_to_falcon(degrees, gear_ratio):
    return degrees / (360 / (gear_ratio * 2048))


def falcon_to_RPM(velocity_counts, gear_ratio):
    motor_RPM = velocity_counts * 600 / 2048
    mech_RPM = motor_RPM / gear_ratio
    return mech_RPM


def RPM_to_falcon(RPM, gear_ratio):
    motor_RPM = RPM * gear_ratio
    sensor_counts = motor_RPM * 2048 / 600
    return sensor_counts


def falcon_to_MPS(velocity_counts, circumference, gearRatio):
    wheel_RPM = falcon_to_RPM(velocity_counts, gearRatio)
    wheel_MPS = (wheel_RPM * circumference) / 60
    return wheel_MPS


def MPS_to_falcon(velocity, circumference, gear_ratio):
    wheel_RPM = velocity * 60 / circumference
    wheel_velocity = RPM_to_falcon(wheel_RPM, gear_ratio)
    return wheel_velocity


def falcon_to_meters(position_counts, circumference, gear_ratio):
    return position_counts * circumference / (gear_ratio * 2048)


def meters_to_falcon(meters, circumference, gear_ratio):
    return meters / (circumference / (gear_ratio * 2048))
