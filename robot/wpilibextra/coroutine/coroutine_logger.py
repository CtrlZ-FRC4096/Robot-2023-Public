from json import dumps
from pathlib import Path

from commands2 import CommandScheduler, CommandBase
import ntcore

from wpilibextra.coroutine.coroutine_robot import CoroutineRobot

def data_from_coroutine(coro) -> list[dict]:
    name = coro.__name__
    filename = Path(coro.gi_code.co_filename).as_posix()
    firstlineno = coro.gi_code.co_firstlineno

    try:
        lineno = coro.gi_frame.f_lineno
    except AttributeError:
        lineno = None

    return [{
        "name": name,
        "filename": filename,
        "firstlineno": firstlineno,
        "lineno": lineno,
    }] + data(coro.gi_yieldfrom)

def data_from_wrapped_coroutine(coro) -> list[dict]:
    try:
        func = coro.gi_frame.f_locals['func']
    except AttributeError:
        return []
    name = func.__name__
    filename = Path(func.__code__.co_filename).as_posix()
    firstlineno = func.__code__.co_firstlineno
    lineno = None


    return [{
        "name": name,
        "filename": filename,
        "firstlineno": firstlineno,
        "lineno": lineno,
    }]

def data(coro) -> list[dict]:
    if coro is None:
        return []

    try:
        filename = Path(coro.gi_code.co_filename).as_posix()
    except AttributeError:
        return []

    if filename.endswith("coroutine_command.py"):
        return data_from_wrapped_coroutine(coro)
    else:
        return data_from_coroutine(coro)

class CoroutineLogger:

    def __init__(self, scheduler: CommandScheduler, robot: CoroutineRobot) -> None:
        self.robot = robot
        self.data = []
        self.publisher = ntcore.NetworkTableInstance.getDefault().getTable("coroutine_logger").getStringTopic("data").publish(options=ntcore.PubSubOptions(keepDuplicates=True, periodic=0.25))
        self.count = 0

        @scheduler.onCommandExecute # type: ignore
        def _(command: CommandBase) -> None:
            if not self.count % 10 == 0:
                return
            try:
                coro = command.__iter__() # type: ignore
            except AttributeError as e:
                try:
                    coro = command.coroutine # type: ignore
                except AttributeError as e2:
                    raise e2 from e

            self.data += data(coro)



    def log(self) -> None:
        self.count += 1
        if not self.count % 10 == 0:
            return
        self.count = 0
        for coro_name in ["_robot_coro", "_autonomous_coro", "_teleop_coro", "_disabled_coro", "_test_coro"]:
            coro = getattr(self.robot, coro_name, None)
            self.data += data(coro)

        self.publisher.set(dumps(self.data))
        # print(self.data)
        self.data.clear()
