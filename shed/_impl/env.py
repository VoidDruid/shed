import inspect
import os
from collections import ChainMap
from types import FrameType
from typing import Any

_ident = object()


def not_exists(obj: Any) -> bool:
    return obj is _ident


env = os.environ


def frame_env(frame: FrameType) -> ChainMap:
    return ChainMap(frame.f_locals, frame.f_globals, env)


def get_var(var: str) -> Any:
    # TODO: default pre-processing
    # TODO: allow function calls and operations in ${}
    caller_frame = inspect.currentframe().f_back  # type:ignore
    value = frame_env(caller_frame).get(var, _ident)
    if not_exists(value):
        raise NameError(f'{var} is neither a script or env variable')
    return value
