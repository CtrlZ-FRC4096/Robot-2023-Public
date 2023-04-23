from typing import TypeVar

T = TypeVar("T")


def ViewOf(obj: T, name=None) -> T:
    class View:
        def __init__(self):
            ...

        def __getattribute__(self, name):
            attr = obj.__getattribute__(name)
            if callable(attr):
                if (
                    name in []
                    or any(
                        name.startswith(prefix)
                        for prefix in [
                            "get",
                            "is",
                            "has",
                            "can",
                            "should",
                            "was",
                            "will",
                            "did",
                            "are",
                            "were",
                            "have",
                            "had",
                            "does",
                            "__",
                            "_",
                        ]
                    )
                    or any(name.endswith(suffix) for suffix in [])
                    or any(isinstance(obj, t) for t in [])
                    or type(obj).__name__ in ["Rotation2d", "Pose2d", "Translation2d"]
                    or any(type(obj).__name__ == t and name == n for t, n in [])
                ):
                    return lambda *args, **kwargs: ViewOf(attr(*args, **kwargs))
                else:
                    raise AttributeError(
                        f"{type(obj).__name__} views are read-only. You cannot call {name}."
                    )

            if isinstance(attr, (int, float, str, bool)):
                return attr

            return ViewOf(attr)

        def __getitem__(self, key):
            attr = obj[key]  # type: ignore
            if callable(attr):
                return lambda *args, **kwargs: ViewOf(attr(*args, **kwargs))
            if isinstance(attr, (int, float, str, bool)):
                return attr
            return ViewOf(attr)

        def __setattr__(self, name, value):
            raise AttributeError(
                f"{type(obj).__name__} views are read-only. You cannot modify {name}."
            )

        def __str__(self):
            return str(obj)

        def __repr__(self):
            return repr(obj)

    v = View()
    return v  # type: ignore
