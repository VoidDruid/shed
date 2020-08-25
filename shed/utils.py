from ast import AST, dump


def pprettify(ast: AST) -> None:
    print(prettify(ast))


def prettify(ast: AST) -> str:
    return dump(ast)
