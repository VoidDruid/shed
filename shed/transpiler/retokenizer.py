"""
Retokenizer parses source code, and transforms it's elements that are
 invalid in python (shell calls) into *syntactically* correct python.

---
Retokenizer works by decomposing source code into tokens, modifying them,
 and then building source code from them again.
It *does not* build python code that can be run - it still needs to be transpiled.
Rationale for this approach is in the docstring for the neighbouring "transpiler.py" module
"""

# TODO: use `tokenize` instead of manipulating strings directly

import re
from typing import Optional

from .context import TranspilerContext

SHELL_CALL_PATTERN = '$({})'
SHELL_CALL_REGEX = re.compile(r'.*?\$\((.*?)\).*?')


def as_call(string: str) -> str:
    return SHELL_CALL_PATTERN.format(string)


def as_const(string: str) -> str:
    return f'"{string}"'


def padded_string(string: str, spaces: int) -> str:
    return ' ' * spaces + string


def retokenize(script_source: str, context: Optional[TranspilerContext]) -> str:
    if context is None:
        context = TranspilerContext()

    strings = script_source.split('\n')
    to_replace = []
    to_insert = []
    for index, string in enumerate(strings):
        matches = re.findall(SHELL_CALL_REGEX, string)
        if not matches:
            continue

        new_string = string
        leading_spaces = len(new_string) - len(new_string.lstrip(' '))

        for match in matches:
            # top-level consts are handled as shell calls
            if as_call(match) == string.lstrip():
                to_replace.append((index, padded_string(as_const(match), leading_spaces)))
                break

            new_id = context.get_new_id()
            to_insert.append((index, padded_string(f'{new_id} = {as_const(match)}', leading_spaces)))

            new_string = new_string.replace(as_call(match), new_id)
        else:
            to_replace.append((index, new_string))

    for index, string in to_replace:
        strings[index] = string

    for counter, (index, string) in enumerate(to_insert):
        strings.insert(index + counter, string)

    result = '\n'.join(strings)
    if result.endswith('\n'):  # There are better ways to do it, but here I like this one
        result = result[:-1]

    context.retokenized = result
    return result
