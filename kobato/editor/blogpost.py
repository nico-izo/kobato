from kobato.editor.abstracteditable import AbstractEditable


class BlogPost(AbstractEditable):

    def __init__(self, *, text='', tags=None, private=False):
        self.text = text
        self.tags = [] if tags is None else tags
        self.private = private

    @property
    def tags(self):
        return self._tags[:]  # you may not modify tags that way

    def add_tag(self, tag):
        self._tags.append(tag.strip())
        return self

    def add_tags(self, tags):
        self._tags.extend([tag.strip() for tag in tags])
        return self

    @tags.setter
    def tags(self, tags):
        self._tags = [tag.strip() for tag in tags]

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text.strip()

    def encode(self):
        to_join = []

        if len(self.tags):
            to_join.append('*' + ', '.join(self.tags))
            to_join.append('')

        to_join.append(self.text)

        return '\n'.join(to_join)

    @classmethod
    def decode(cls, string):
        """
        In current implementation you cannot encode information about
        private post in string. So you should manually set
        post.private = True in case of private post
        """
        i = 0
        result = {
            'text': '',
            'tags': [],
            'private': False
        }

        lines = string.strip().splitlines(True)

        array_to_join = []
        for line in lines:
            if i == 0 and line.startswith('*'):
                result['tags'] = [s.strip() for s in line[1:].split(",")]
            else:
                array_to_join.append(line)
            i += 1

        result['text'] = "".join(array_to_join).strip()

        return cls(**result)

    def reload(self, string):
        new = BlogPost.decode(string)

        self._tags = new._tags
        self._text = new._text
