from ast import AST, dump
from typing import Any

import astpretty
from rich.console import Console

console = Console()


def prettify(ast: AST) -> str:
    try:
        return astpretty.pformat(ast, show_offsets=False)
    except Exception:  # pylint:disable=broad-except
        return dump(ast)


def pprettify(ast: AST) -> None:
    console.print(prettify(ast))


def title(string: Any) -> str:
    return f'[blue]{string}[/blue]'


def info(string: Any) -> str:
    return f'[green]{string}[/green]'


def error(string: Any) -> str:
    return f'[red]{string}[/red]'


def line() -> str:
    return '-' * console.width


def print_line() -> None:
    console.print(line())


def center(string: str) -> str:
    return ' ' * ((console.width - len(string)) // 2) + string


def print_center(string: str) -> None:
    console.print(center(string))


def print_padded(string: str, ident: int = 0) -> None:
    console.print('\t' * ident + string)
