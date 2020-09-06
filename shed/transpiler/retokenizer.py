"""
Retokenizer parses source code, and transforms it's elements that are
 invalid in python (shell calls) into *syntactically* correct python.

---
Retokenizer works by parsing and modifying source code, looking for shell-specific syntax.
It *does not* build python code that can be run - it still needs to be transpiled.
Rationale for this approach is in the docstring for the neighbouring "transpiler.py" module
"""

import re
from typing import List, Optional, Tuple

from .context import TranspilerContext
from .utils import SHELL_CALL_REGEX, SHELL_VAR_REGEX, as_call, as_const, as_var, padded_string


def retokenize(script_source: str, context: Optional[TranspilerContext] = None) -> str:
    if context is None:
        context = TranspilerContext()

    strings = script_source.split('\n')

    to_replace, to_insert = parse_strings(strings, context)

    for index, string in to_replace:
        strings[index] = string

    for counter, (index, string) in enumerate(to_insert):
        strings.insert(index + counter, string)

    result = '\n'.join(strings)
    if result.endswith('\n'):  # There are better ways to do it, but here I like this one
        result = result[:-1]

    context.retokenized = result
    return result


def parse_strings(
    strings: List[str], context: Optional[TranspilerContext] = None
) -> Tuple[List[Tuple[int, str]], List[Tuple[int, str]]]:
    if context is None:
        context = TranspilerContext()

    to_replace: List[Tuple[int, str]] = []
    to_insert: List[Tuple[int, str]] = []

    for index, string in enumerate(strings):
        new_string = string
        leading_spaces = len(new_string) - len(new_string.lstrip(' '))

        def replace_matches(
            matches: List[str], index_: int = index, leading_spaces_: int = leading_spaces
        ) -> None:
            nonlocal new_string
            for match in matches:
                new_id = context.get_new_id()  # type:ignore
                new_string = new_string.replace(match, new_id)
                to_insert.append(
                    (index_, padded_string(f'{new_id} = {as_const(match)}', leading_spaces_))
                )

        var_matches = [as_var(m) for m in re.findall(SHELL_VAR_REGEX, new_string)]
        replace_matches(var_matches)

        call_matches = [as_call(m) for m in re.findall(SHELL_CALL_REGEX, new_string)]
        # top-level consts are handled as shell calls
        if len(call_matches) == 1:
            only_match = call_matches[0]
            if only_match == string.lstrip():
                to_replace.append((index, padded_string(as_const(only_match), leading_spaces)))
                continue
        replace_matches(call_matches)

        to_replace.append((index, new_string))

    return to_replace, to_insert
