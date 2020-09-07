from typing import List


def norm(value: bytes) -> List[str]:
    result = value.decode().split('\n')

    if result[-1] == '':  # TODO: can there be cases where trailing '' is NOT from trailing '\n'?
        result = result[:-1]

    return result
