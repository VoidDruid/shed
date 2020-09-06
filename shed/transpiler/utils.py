import re


def strip_shell_syntax(string: str) -> str:
    return string[2:-1]  # remove leading $[{,(] and ending [},)]


SHELL_CALL_PATTERN = '$({})'
SHELL_VAR_PATTERN = '${{{}}}'
SHELL_CALL_REGEX = re.compile(r'.*?\$\((.*?)\).*?')
SHELL_VAR_REGEX = re.compile(r'.*?\${(.*?)\}.*?')


def as_call(string: str) -> str:
    return SHELL_CALL_PATTERN.format(string)


def as_var(string: str) -> str:
    return SHELL_VAR_PATTERN.format(string)


def as_const(string: str) -> str:
    return f'"""{string}"""'


def padded_string(string: str, spaces: int) -> str:
    return ' ' * spaces + string
