import io
from ast import AST, parse
from typing import Optional, TextIO, Union

from .transpiler import transpile as transpile_


def ast_from_filename(filename: str) -> AST:
    # TODO: maybe we can import it as module or something?
    with open(filename, 'r') as script_file:
        return ast_from_source_text(script_file.read())


def ast_from_source_text(source: str) -> AST:
    return parse(source)


def transpile(file: Optional[Union[str, TextIO]] = None, source: Optional[str] = None) -> AST:
    assert (
        file or source
    ), 'Provide either opened file (or file name) or source code for transpiling, not both!'

    if isinstance(file, io.TextIOWrapper):
        source = file.read()
    if source is not None:
        script_ast = ast_from_source_text(source)
    else:
        script_ast = ast_from_filename(file)  # type:ignore

    return transpile_(script_ast)


__all__ = ['transpile']
