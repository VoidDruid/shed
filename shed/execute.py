# pylint: disable=W0122

from ast import AST
from typing import Any, Dict, Optional

from .transpiler import TranspilerContext


def execute(script: AST, config: Optional[TranspilerContext] = None) -> None:
    if config:
        filename = config.filename
    else:
        filename = TranspilerContext.DEFAULT_FILENAME

    # globals and locals for `exec` need to be the same dict, so that it thinks it runs in a module
    env_substitution: Dict[str, Any] = {}
    # TODO: optimize??, add some checks, handle exit code,
    #  maybe special handling for streams, pipes, etc. - a lot of stuff
    exec(compile(script, filename=filename, mode='exec'), env_substitution, env_substitution)
