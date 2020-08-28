# pylint: disable=W0122

from ast import AST


def execute(script: AST) -> None:
    # TODO: optimize??, add some checks, handle exit code,
    #  maybe special handling for streams, pipes, etc. - a lot of stuff
    exec(compile(script, filename='', mode='exec'))
