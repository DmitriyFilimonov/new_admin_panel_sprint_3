from functools import wraps
from typing import Generator


def coroutine(func):
    @wraps(func)
    def start(*args, **kwargs) -> Generator:
        gen = func(*args, **kwargs)
        next(gen)  # запускаем генератор до первого yield
        return gen
    return start