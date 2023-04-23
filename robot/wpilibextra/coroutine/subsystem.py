from typing import Callable, Generator, Union, overload

from commands2 import Command
from commands2 import SubsystemBase as _SubsystemBase

from ..coroutine.coroutine_command import CoroutineCommand, ensure_generator_function


class _Unset:
    pass


Unset = _Unset()

Coroutineable = Union[
    Callable[[], None],
    Callable[[], Generator[None, None, None]],
    Generator[None, None, None],
]


class SubsystemBase(_SubsystemBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # def setDefaultCommand(self, defaultCommand: Command) -> None:
    #     return super().setDefaultCommand(defaultCommand)

    @overload
    def setDefaultCommand(self, defaultCommand: Command, /) -> None:
        ...

    @overload
    def setDefaultCommand(
        self, coroutine: Union[Coroutineable, _Unset] = Unset, /
    ) -> Callable[[Coroutineable], None]:
        ...

    def setDefaultCommand(
        self, *args, **kwargs
    ) -> Union[Callable[[Coroutineable], None], None]:
        coc = None
        if args:
            coc = args[0]
        if coc == None:

            def wrapper(coroutine: Coroutineable) -> None:
                return self.setDefaultCommand(coroutine, **kwargs)  # type: ignore

            return wrapper

        if not callable(coc):
            return super().setDefaultCommand(*args, **kwargs)

        command = CoroutineCommand(
            ensure_generator_function(coc),
            requirements=kwargs.get("requirements", [self]),
            interruptible=kwargs.get("interruptible", True),
        )
        return super().setDefaultCommand(command)
