import math

from wpimath._wpimath import inputModulus

seconds = float

class PIDD2Controller:

    def __init__(
        self,
        p: float,
        i: float,
        d: float,
        d2: float,
        period: seconds = 0.02,
    ):
        self.p = p
        self.i = i
        self.d = d
        self.d2 = d2
        self.period = period

        self.maximum_integral = 1.0
        self.minimum_integral = -1.0
        self.maximum_input = 0
        self.minimum_input = 0

        self.is_continuous = False

        self.position_tolerance = 0.05
        self.velocity_tolerance = math.inf

        self.setpoint: float | None = None

        self.prev_m: float | None = None
        self.prev_m1: float | None = None
        self.prev_e: float | None = None
        self.prev_e1: float | None = None
        self.e_1 = 0

        self.is_using_PV_D = True
        self.is_using_PV_D2 = True

        if self.period <= 0:
            raise ValueError("Controller period must be a non-zero positive number!")

    def setPID(self, p: float, i: float, d: float, d2: float) -> None:
        self.p = p
        self.i = i
        self.d = d
        self.d2 = d2

    def setP(self, p: float) -> None:
        self.p = p

    def setI(self, i: float) -> None:
        self.i = i

    def setD(self, d: float) -> None:
        self.d = d

    def setD2(self, d2: float) -> None:
        self.d2 = d2

    def getP(self) -> float:
        return self.p

    def getI(self) -> float:
        return self.i

    def getD(self) -> float:
        return self.d

    def getD2(self) -> float:
        return self.d2

    def getPeriod(self) -> seconds:
        return self.period

    def getPositionTolerance(self) -> float:
        return self.position_tolerance

    def getVelocityTolerance(self) -> float:
        return self.velocity_tolerance

    def setSetpoint(self, setpoint: float) -> None:
        self.setpoint = setpoint

    def getSetpoint(self) -> float:
        return self.setpoint # type: ignore

    def atSetpoint(self) -> bool:
        return self.prev_m is not None and self.setpoint is not None and abs(self.prev_e or 0) < self.position_tolerance and abs(self.prev_e1 or 0) < self.velocity_tolerance

    def enableContinuousInput(self, minimum_input: float, maximum_input: float) -> None:
        self.is_continuous = True
        self.minimum_input = minimum_input
        self.maximum_input = maximum_input

    def disableContinuousInput(self) -> None:
        self.is_continuous = False

    def isContinuousInputEnabled(self) -> bool:
        return self.is_continuous

    def enableMeasurementD(self) -> None:
        self.is_using_PV_D = True

    def disableMeasurementD(self) -> None:
        self.is_using_PV_D = False

    def isMeasurementDEnabled(self) -> bool:
        return self.is_using_PV_D

    def enableMeasurementD2(self) -> None:
        self.is_using_PV_D2 = True

    def disableMeasurementD2(self) -> None:
        self.is_using_PV_D2 = False

    def isMeasurementD2Enabled(self) -> bool:
        return self.is_using_PV_D2

    def setIntegratorRange(self, minimum_integral: float, maximum_integral: float) -> None:
        self.minimum_integral = minimum_integral
        self.maximum_integral = maximum_integral

    def setTolerance(self, position_tolerance: float, velocity_tolerance: float = math.inf) -> None:
        self.position_tolerance = position_tolerance
        self.velocity_tolerance = velocity_tolerance

    def getPositionError(self) -> float:
        return self.prev_e or 0

    def getVelocityError(self) -> float:
        return self.prev_e1 or 0

    def calculate(self, measurement: float, setpoint: float | None = None) -> float:
        if setpoint is not None:
            self.setpoint = setpoint
        elif self.setpoint is None:
            self.setpoint = measurement

        # m is measurement, e is error
        # Pretend the suffixes are exponents in the laplace domain
        # so m1 is derivative, m_1 is integral, etc.

        m = measurement

        if self.is_continuous:
            error_bound = (self.maximum_input - self.minimum_input) / 2.0
            e = inputModulus(self.setpoint - m, -error_bound, error_bound)
        else:
            e = self.setpoint - m

        if self.i != 0:
            self.e_1 = max(self.minimum_integral * self.i,
                min(self.e_1 + e * self.period,
                self.maximum_integral * self.i))


        prev_e = e if self.prev_e is None else self.prev_e
        prev_m = m if self.prev_m is None else self.prev_m

        e1 = (e - prev_e) / self.period
        m1 = (m - prev_m) / self.period

        prev_e1 = e1 if self.prev_e1 is None else self.prev_e1
        prev_m1 = m1 if self.prev_m1 is None else self.prev_m1
        e2 = (e1 - prev_e1) / self.period
        m2 = (m1 - prev_m1) / self.period

        self.prev_e = e
        self.prev_m = m
        self.prev_e1 = e1
        self.prev_m1 = m1

        d_val = -m1 if self.is_using_PV_D else e1
        d2_val = -m2 if self.is_using_PV_D2 else e2

        return self.p * e + self.i * self.e_1 + self.d * d_val + self.d2 * d2_val

    def reset(self) -> None:
        self.prev_m = None
        self.prev_e = None
        self.prev_m1 = None
        self.prev_e1 = None
        self.e_1 = 0