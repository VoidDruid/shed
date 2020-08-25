import os
import sys
from typing import Any

import click
from click_spinner import spinner
from rich.console import Console

from . import __lang_extension__, __lang_name__, __version__
from .config import settings
from .run import execute
from .transpiler import transpile
from .utils import prettify

VERBOSITY_NUM_TO_STR = {
    1: 'info',
    2: 'develop',
    3: 'debug',
}

console = Console()


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


def iprint(string: str, ident: int = 0) -> None:
    console.print('\t' * ident + string)


def is_filename(script: str) -> bool:
    return script.endswith(__lang_extension__)


@click.command(f'Run {__lang_name__} script')
@click.argument('script', nargs=1, required=True)
@click.option('-v', '--verbose', count=True)
@click.option('-t', '--transpile', 'only_transpile', is_flag=True, default=False)
def main(script: str, only_transpile: bool, verbose: int) -> None:
    script = script.strip()

    if verbose:
        console.print(f'Verbosity: {info(VERBOSITY_NUM_TO_STR[verbose])}')
        console.print(f'Processing: {info(script)}')
        console.print()
    if verbose == 2:
        console.print(title(f'{__lang_name__.upper()} info'))
        iprint(f'Version {info(__version__)}', 1)
        for name, value in settings:
            iprint(f'{name}: {info(value)}', 1)
        console.print()

    with spinner():
        if is_filename(script):
            with open(script, 'r') as script_file:
                result_script = transpile(file=script_file)
        else:
            result_script = transpile(source=script)

    if verbose:
        print_line()

    if only_transpile:
        print_center(title(os.path.basename(script)))
        console.print(prettify(result_script), highlight=False)
        sys.exit(0)

    execute(result_script)

    sys.exit(0)


if __name__ == '__main__':
    # pylint: disable=E1120
    main()
