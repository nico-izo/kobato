import subprocess
import tempfile
import os

from datetime import datetime
from copy import deepcopy
from kobato.misc import get_data_dir


class TextEditorException(Exception):
    pass


class TextEditor:

    def __init__(self, obj, filename=None):
        self._editable = deepcopy(obj)
        self._editor = 'sensible-editor'

        self._filename = filename
        self._file = None

    @classmethod
    def load(cls, filename, codec):
        """
        :param filename path to file
        :param codec class, inherited from kobato.editor.abstracteditable
        :rtype TextEditor
        """

        with open(filename) as f:
            return cls(codec.decode(f.read()), filename=filename)

    def result(self):
        return self._editable

    def run(self):
        if self._file is None:
            raise TextEditorException('You must run() editor only in `with` block')

        subprocess.call([self._editor, self._file.name])

        self._file.seek(0)
        self._editable.reload(self._file.read())

    def save(self, to_dir=None, name='waifu_draft_%Y-%m-%dT%H_%M_%S.txt'):
        if to_dir is None:
            to_dir = get_data_dir()
        out_draft = os.path.join(to_dir, datetime.now().strftime(name))

        with open(out_draft, mode='wt', encoding='utf8') as f:
            f.write(self._editable.encode())

        return out_draft

    def __enter__(self):
        if self._file is not None:
            raise TextEditorException('Nested with blocks not allowed')

        filename = self._filename

        if filename is not None:
            self._file = open(filename, mode='w+t', encoding='utf8')
        else:
            self._file = tempfile.NamedTemporaryFile(mode='w+t', encoding='utf8')
            self._file.write(self._editable.encode())
            self._file.flush()
            os.fsync(self._file.fileno())
            self._file.seek(0)

        return self

    def __exit__(self, type_, value, traceback):
        self._file.close()
        self._file = None
