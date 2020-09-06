import sys

import click

from . import __lang_extension__, __lang_name__, __version__
from .config import settings
from .execute import execute
from .transpiler import TranspilerContext, transpile
from .utils import console, info, prettify, print_center, print_line, print_padded, title

VERBOSITY_NUM_TO_STR = {
    1: 'info',
    2: 'develop',
    3: 'debug',
}


def is_filename(script: str) -> bool:
    return script.endswith(__lang_extension__)


@click.command(f'Run {__lang_name__} script')
@click.argument('script', nargs=1, required=True)
@click.option('-v', '--verbose', count=True)
@click.option('-t', '--transpile', 'show_transpiled', is_flag=True, default=False)
@click.option('-r', '--run', 'run_anyway', is_flag=True, default=False)
def main(  # pylint:disable=R0915
    script: str, show_transpiled: bool, run_anyway: bool, verbose: int
) -> None:
    script = script.strip()
    context = TranspilerContext(verbosity=verbose,)

    if verbose:
        console.print(f'Verbosity: {info(f"{VERBOSITY_NUM_TO_STR[verbose]} ({verbose})")}')
        console.print(f'Processing: {info(script)}')
        console.print()
    if verbose >= 2:
        console.print(title(f'{__lang_name__.upper()} info'))
        print_padded(f'Version {info(__version__)}', 1)
        for name, value in settings:
            print_padded(f'{name}: {info(value)}', 1)
        console.print()

    if is_filename(script):
        context.set_filename(script)
        with open(script, 'r') as script_file:
            result_script_ast = transpile(file=script_file, context=context)
    else:
        result_script_ast = transpile(source=script, context=context)

    # pylint: disable=no-member
    if context.verbosity >= 2:  # type:ignore
        print_line()
        print_center(title('Retokenized'))
        console.print(context.retokenized, highlight=False)

    if show_transpiled:
        print_line()
        print_center(title('Transpiled'))
        console.print(prettify(result_script_ast), highlight=False)
        if not run_anyway:
            sys.exit(0)

    if show_transpiled or verbose:
        print_line()
        print_center(title('Execution'))

    execute(result_script_ast, context)
    sys.exit(0)


if __name__ == '__main__':
    # pylint: disable=E1120
    main()
