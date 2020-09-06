import subprocess as sb
from typing import Any, List, Optional, Dict

from ..std import norm


def process_result(result: bytes, args: List[str]) -> List[str]:
    # TODO: smarter default processing
    return norm(result)


def create_call_args(args: List[str], get_output: bool) -> Dict[str, Any]:
    # TODO, FIXME: get rid of shell=True, handle pipes as special case

    args_dict = {'shell': False}

    if '|' in args:
        args_dict['shell'] = True
        args_dict['args'] = ' '.join(args)
    else:
        args_dict['args'] = args

    return args_dict


def call(args: List[str], get_output: Optional[bool] = False) -> Any:
    # TODO: handle non-zero exit codes
    method = getattr(sb, 'check_output' if get_output else 'call')  # TODO, FIXME: seems sketchy

    result = method(**create_call_args(args, get_output))

    if get_output:
        return process_result(result, args)
    return result
