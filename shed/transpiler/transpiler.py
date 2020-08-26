# TODO: REFACTOR THIS MODULE, IT WAS A QUICK AND DIRTY PROTOTYPE

import re
from ast import AST, NodeTransformer, Module, Import, alias, parse, Name, Expr, Call, Attribute, Load, copy_location, \
    fix_missing_locations, Constant, Assign, walk, iter_child_nodes
from ast import List as ASTList
from typing import Any, Optional, Union

from ..utils import console, print_center, print_line, title

SHELL_CALL_REGEX = re.compile(r'.*?`(.*?)`.*?')


class TranspilerContext:
    DEFAULT_FILENAME = '__shed_script'
    filename: str
    prefix: str
    fields = {'verbosity'}

    def __init__(self, filename: Optional[str] = None, **kwargs) -> None:
        assert len(set(kwargs.keys()) - self.fields) == 0, 'Unexpected fields provided for TranspilerContext'
        for name, value in kwargs.items():
            setattr(self, name, value)

        self.id_counter = -1
        self.set_filename(filename)

    def set_filename(self, filename: Optional[str] = None) -> None:
        if self.id_counter != -1:
            raise RuntimeError('Some IDs were already generated from this context, can not modify it!')

        self.filename = filename or self.DEFAULT_FILENAME

        prefix = self.filename.replace('.', '_')
        if not self.filename.startswith('__'):
            prefix = f'__{prefix}'
        self.prefix = prefix

    def get_new_id(self) -> str:
        self.id_counter += 1
        return self.prefix + '_var_' + str(self.id_counter)


def transpile_source(script_source: str, context: Optional[TranspilerContext]) -> AST:
    if context is None:
        context = TranspilerContext()

    strings = script_source.split('\n')
    to_replace = []
    to_insert = []
    for index, string in enumerate(strings):
        matches = re.findall(SHELL_CALL_REGEX, string)
        if not matches:
            continue

        new_string = string
        leading_spaces = len(new_string) - len(new_string.lstrip(' '))

        for match in matches:
            # TODO: default preprocessing
            if f'`{match}`' == string:
                to_replace.append((index, f'"{match}"'))  # top-level consts are handled as shell calls
                break

            new_id = context.get_new_id()
            to_insert.append((index, ' ' * leading_spaces + f'{new_id} = {match}'))

            new_string = new_string.replace(f'`{match}`', new_id)
        else:
            to_replace.append((index, new_string))

    for index, string in to_replace:
        strings[index] = string

    for index, string in to_insert:
        strings.insert(index, string)

    prepared_script = '\n'.join(strings)
    if context.verbosity >= 2:
        print_line()
        print_center(title('Prepared script'))
        console.print(prepared_script, highlight=False)

    return transpile_ast(parse(prepared_script), context)


sb_name = '__sb__'
subprocess_import = Import(names=[alias(name='subprocess', asname=sb_name)])
subprocess_import.lineno = 1
subprocess_import.col_offset = 1


class ShellCallTransformer(NodeTransformer):
    def __init__(self, context: TranspilerContext):
        self.context = context

    def generic_visit(self, node: AST) -> Optional[AST]:
        for child in iter_child_nodes(node):
            child.parent = node
        return super().generic_visit(node)

    def visit_Module(self, node: Module) -> Any:
        node.body.insert(0, subprocess_import)
        return self.generic_visit(node)

    @staticmethod
    def replace_with_call(node: Union[Name, Constant], get_output: bool = True) -> Any:
        if isinstance(node, Name):
            values = [node.id]
        elif isinstance(node, Constant):
            values = node.value.split(' ')
        else:
            raise ValueError('Accepted nodes are Names and Constants')

        args = [ASTList(elts=[Constant(value=val, kind=None) for val in values], ctx=Load())]
        method = 'check_output' if get_output else 'call'
        func = Attribute(value=Name(id=sb_name, ctx=Load()), ctx=Load(), attr=method)

        expr = Call(func=func, args=args, keywords=[])
        expr = copy_location(expr, node)

        return expr

    @staticmethod
    def is_top_level(node: AST) -> bool:
        if isinstance(node, Module):
            return True
        # either has a module as a parent, or as grandparent - then should be wrapped in expr
        if parent := getattr(node, 'parent', None):
            if isinstance(parent, Module):
                return True
            if isinstance(parent, Expr):
                if grandparent := getattr(parent, 'parent', None):
                    if isinstance(grandparent, Module):
                        return True
        return False

    def visit_Name(self, node: Name) -> Any:
        # 'Name' is top-level expr by itself - it should be a shell call
        if self.is_top_level(node):
            return self.replace_with_call(node, get_output=False)
        return node

    visit_Constant = visit_Name  # TODO: do we need any other checks?

    def visit_Assign(self, node: Assign) -> Any:
        # if assigning to autogenerated variable
        if len(node.targets) == 1 and node.targets[0].id.startswith(self.context.prefix):
            node.value = self.replace_with_call(node.value)
        return node


def transpile_ast(script_ast: AST, context: Optional[TranspilerContext] = None) -> AST:
    if context is None:
        context = TranspilerContext()

    transformer = ShellCallTransformer(context)

    result_ast = transformer.visit(script_ast)
    fix_missing_locations(result_ast)
    return result_ast
