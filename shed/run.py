# pylint: disable=W0122

from ast import AST


def execute(script: AST) -> None:
    exec(compile(script, filename='', mode='exec'))  # TODO: optimize?
