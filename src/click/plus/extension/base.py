import abc
class ExtensionError(Exception):
    pass


class ExtensionNotFound(ExtensionError):
    pass


class ExtensionBase(abc.ABC):
    @classmethod
    def get(cls, name):
        classes = {}
        def walk(klasses):
            for c in klasses:
                if c.__subclasses__():        
                    walk(c.__subclasses__())
                classes[getattr(c, "NAME", c.__name__)] = c
        walk(cls.__subclasses__())

        names = { c.lower(): c for c in classes }
        if name.lower() not in names:
            raise ExtensionNotFound(f"no class found for name={name}, allowed={', '.join(classes) or 'none'}")
        return classes[names[name]]

    def __init__(self, name, dependencies=None):
        self.name = name

    @abc.abstractmethod
    def setup(self, fn, arguments):
        print(f"This is the ExtensionBase.setup(fn, arguments={arguments})")
        return fn

    @abc.abstractmethod
    def process(self, kwargs, arguments):
        print(f"This is the ExtensionBase.process(kwargs={kwargs}, arguments={arguments})")

