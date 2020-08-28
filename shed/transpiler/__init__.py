import io
from ast import AST
from typing import Optional, TextIO, Union

from .context import TranspilerContext
from .retokenizer import retokenize
from .transpiler import SUBPROCESS_NAME, transpile_ast, transpile_source


def source_from_filename(filename: str) -> str:
    with open(filename, 'r') as script_file:
        return script_file.read()


def validate(source: str, context: TranspilerContext) -> None:
    reserved_names = (SUBPROCESS_NAME, context.prefix)
    for name in reserved_names:
        if name in source:  # TODO, FIXME: very dumb check
            raise ValueError(f'Found reserved name/prefix {name}')
    if '\n\t' in source:
        raise ValueError('Tabs are forbidden! Use spaces for indentation')


def transpile(
    file: Optional[Union[str, TextIO]] = None,
    source: Optional[str] = None,
    context: Optional[TranspilerContext] = None,
) -> AST:
    assert (
        file or source
    ), 'Provide either opened file (or file name) or source code for transpiling, not both!'
    filename = None

    if isinstance(file, io.TextIOWrapper):
        source = file.read()
        filename = file.name
    if source is None:
        source = source_from_filename(file)  # type: ignore
        filename = file  # type: ignore

    context = context or TranspilerContext(filename=filename)
    validate(source, context)
    return transpile_source(source, context)


__all__ = ['transpile_ast', 'transpile', 'validate', 'TranspilerContext', 'retokenize']
