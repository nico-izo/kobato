from kobato.editor.abstracteditable import AbstractEditable


class SimpleText(AbstractEditable):

    def __init__(self, text=''):
        self.text = text

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text.strip()

    def encode(self):
        return self.text

    @classmethod
    def decode(cls, string):
        return cls(string)

    def reload(self, string):
        new = SimpleText.decode(string)

        self._text = new._text
