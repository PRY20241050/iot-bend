from typing import Callable, TypeVar

T = TypeVar("T")


def split_string(
    string: str, separator: str = ",", conversion_type: Callable[[str], T] = int
) -> list[T]:
    return [conversion_type(element) for element in string.split(separator)] if string else []
