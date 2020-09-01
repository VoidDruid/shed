from typing import List


def norm(value: bytes) -> List[str]:
    return value.decode().split('\n')
