from typing import Any, Optional

from ..config import __lang_name__


class TranspilerContext:
    DEFAULT_FILENAME = f'{__lang_name__}_script'
    filename: str
    prefix: str
    fields = {'verbosity'}

    def __init__(self, filename: Optional[str] = None, **kwargs: Any) -> None:
        assert (
            len(set(kwargs.keys()) - self.fields) == 0
        ), 'Unexpected fields provided for TranspilerContext'
        for name, value in kwargs.items():
            setattr(self, name, value)

        self.retokenized: Optional[str] = None
        self.id_counter = -1
        self.set_filename(filename)

    def set_filename(self, filename: Optional[str] = None) -> None:
        if self.id_counter != -1:
            raise RuntimeError(
                'Some IDs were already generated from this context, can not modify it!'
            )

        self.filename = filename or self.DEFAULT_FILENAME

        prefix = self.filename.replace('.', '_')
        if not self.filename.startswith('__'):
            prefix = f'__{prefix}'
        self.prefix = prefix

    def get_new_id(self) -> str:
        self.id_counter += 1
        return self.prefix + '_var_' + str(self.id_counter)
