from functools import wraps
from typing import Any, Callable, Generator, List, Union, overload

from commands2 import Command, Subsystem
from commands2.button import Button as _Button

from ..coroutine import CoroutineCommand
from ..coroutine.coroutine_command import ensure_generator_function


class _Unset:
    pass


Unset = _Unset()

Coroutineable = Union[
    Callable[[], None],
    Callable[[], Generator[None, None, None]],
    Generator[None, None, None],
]


class Button(_Button):
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.__bool__()


class CustomButton(Button):
    # new ones

    @overload
    def whenHeld(
        self,
        coroutine: Union[Coroutineable, _Unset] = Unset,
        /,
        *,
        interruptible: bool = True,
        requirements: List[Subsystem] = [],
    ) -> Union[Button, Callable[[Coroutineable], Button]]:
        ...

    @overload
    def whenPressed(
        self,
        coroutine: Union[Coroutineable, _Unset] = Unset,
        /,
        *,
        interruptible: bool = True,
        requirements: List[Subsystem] = [],
    ) -> Union[Button, Callable[[Coroutineable], Button]]:
        ...

    @overload
    def whenReleased(
        self,
        coroutine: Union[Coroutineable, _Unset] = Unset,
        /,
        *,
        interruptible: bool = True,
        requirements: List[Subsystem] = [],
    ) -> Union[Button, Callable[[Coroutineable], Button]]:
        ...

    @overload
    def whileHeld(
        self,
        coroutine: Union[Coroutineable, _Unset] = Unset,
        /,
        *,
        interruptible: bool = True,
        requirements: List[Subsystem] = [],
    ) -> Union[Button, Callable[[Coroutineable], Button]]:
        ...

    # existing ones
    @overload
    def whenHeld(self, command: Command, /, interruptible: bool = True) -> Button:
        ...

    @overload
    def whenPressed(self, command: Command, /, interruptible: bool = True) -> Button:
        ...

    @overload
    def whenReleased(self, command: Command, /, interruptible: bool = True) -> Button:
        ...

    @overload
    def whileHeld(self, command: Command, /, interruptible: bool = True) -> Button:
        ...

    # new defs

    def whenHeld(self, *args, **kwargs) -> Any:
        coc = None
        if args:
            coc = args[0]
        if coc == None:

            def wrapper(coroutine: Coroutineable) -> Button:
                # __import__("code").interact(local={**locals(), **globals()})
                return self.whenHeld(coroutine, **kwargs)  # type: ignore

            return wrapper

        if not callable(coc):
            return super().whenHeld(*args, **kwargs)

        # __import__("code").interact(local={**locals(), **globals()})

        command = CoroutineCommand(
            ensure_generator_function(coc),
            requirements=kwargs.get("requirements", []),
            interruptible=kwargs.get("interruptible", True),
        )
        return super().whenHeld(command)

    def whenPressed(self, *args, **kwargs) -> Any:
        coc = None
        if args:
            coc = args[0]
        if coc == None:

            def wrapper(coroutine: Coroutineable) -> Button:
                # __import__("code").interact(local={**locals(), **globals()})
                return self.whenPressed(coroutine, **kwargs)  # type: ignore

            return wrapper

        if not callable(coc):
            return super().whenPressed(*args, **kwargs)

        # __import__("code").interact(local={**locals(), **globals()})

        command = CoroutineCommand(
            ensure_generator_function(coc),
            requirements=kwargs.get("requirements", []),
            interruptible=kwargs.get("interruptible", True),
        )
        return super().whenPressed(command)

    def whenReleased(self, *args, **kwargs) -> Any:
        coc = None
        if args:
            coc = args[0]
        if coc == None:

            def wrapper(coroutine: Coroutineable) -> Button:
                return self.whenReleased(coroutine, **kwargs)  # type: ignore

            return wrapper

        if not callable(coc):
            return super().whenReleased(*args, **kwargs)

        # __import__("code").interact(local={**locals(), **globals()})

        command = CoroutineCommand(
            ensure_generator_function(coc),
            requirements=kwargs.get("requirements", []),
            interruptible=kwargs.get("interruptible", True),
        )
        return super().whenReleased(command)

    def whileHeld(self, *args, **kwargs) -> Any:
        coc = None
        if args:
            coc = args[0]
        if coc == None:

            def wrapper(coroutine: Coroutineable) -> Button:
                return self.whileHeld(coroutine, **kwargs)  # type: ignore

            return wrapper

        if not callable(coc):
            return super().whileHeld(*args, **kwargs)

        command = CoroutineCommand(
            coc(),
            requirements=kwargs.get("requirements", []),
            interruptible=kwargs.get("interruptible", True),
        )
        return super().whileHeld(command)
