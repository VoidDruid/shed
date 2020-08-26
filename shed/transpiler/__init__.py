import io
from ast import AST
from typing import Optional, TextIO, Union

from .transpiler import transpile_source, transpile_ast, TranspilerContext, sb_name


def source_from_filename(filename: str) -> str:
    with open(filename, 'r') as script_file:
        return script_file.read()


def validate_source(source: str, context: TranspilerContext) -> None:
    reserved_names = (sb_name, context.prefix)
    for name in reserved_names:
        if name in source:  # TODO, FIXME: very dumb check
            raise ValueError(f'Found reserved name/prefix {name}')
    if '\n\t' in source:
        raise ValueError('Tabs are forbidden! Use spaces for indentation')


def transpile(
    file: Optional[Union[str, TextIO]] = None,
    source: Optional[str] = None,
    context: Optional[TranspilerContext] = None
) -> AST:
    assert (
        file or source
    ), 'Provide either opened file (or file name) or source code for transpiling, not both!'
    filename = None

    if isinstance(file, io.TextIOWrapper):
        source = file.read()
        filename = file.name
    if source is None:
        source = source_from_filename(file)
        filename = file

    context = context or TranspilerContext(filename=filename)
    validate_source(source, context)
    return transpile_source(source, context)


__all__ = ['transpile_source', 'transpile_ast', 'transpile', 'validate_source', 'TranspilerContext']
