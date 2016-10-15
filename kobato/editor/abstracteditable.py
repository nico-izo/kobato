class AbstractEditable:
    """
    Abstract mixin class with three mandatory methods:
        decode (classmethod string parser)
        encode (renderer of object to string)
        reload (same as decode, but not a classmethod)
    """

    def encode(self):
        """
        Serialize object in human-readable string,
        which would be displayed in text editor (e.g. vim)
        """
        raise NotImplementedError

    @classmethod
    def decode(cls, string):
        """
        Custom constructor.
        parse result string of encode() back to object.
        """
        raise NotImplementedError

    def reload(self, string):
        """
        Same as decode, but as method of instance
        """
        raise NotImplementedError
