import abc
import sys
import inspect


class ExtensionError(Exception):
    pass


class ExtensionDevelopmentError(ExtensionError):
    pass


class ExtensionNotFound(ExtensionError):
    pass


def walk_classes(klasses, classes):
    for c in klasses:
        if c.__subclasses__():
            walk_classes(c.__subclasses__(), classes)
        # the class name is either the __class__.__name__
        # or the __class__.NAME lowered
        name = getattr(c, "NAME", c.__name__)
        if name.lower() in classes:
            raise ExtensionDevelopmentError(
                f"duplicate name for extension {name}",
                inspect.getfile(c), inspect.getfile(classes[name.lower()])
            )
        classes[name.lower()] = c


class ExtensionBase(abc.ABC):
    classes = None

    @classmethod
    def get(cls, name, reload=False):
        if reload:
            ExtensionBase.classes = None

        if ExtensionBase.classes is None:
            ExtensionBase.classes = {}
            walk_classes(cls.__subclasses__(), ExtensionBase.classes)

        if name.lower() not in ExtensionBase.classes:
            raise ExtensionNotFound(f"no class found for name={name}",
                                    ', '.join(ExtensionBase.classes) or 'none')
        return ExtensionBase.classes[name.lower()]

    def __init__(self, name, dependencies=None):
        self.name = name

    @abc.abstractmethod
    def setup(self, fn, arguments):
        print(f"This is the ExtensionBase.setup(fn, arguments={arguments})",
              file=sys.stderr)
        return fn

    @abc.abstractmethod
    def process(self, kwargs, arguments):
        print((
            f"This is the ExtensionBase.process(kwargs={kwargs},"
            f" arguments={arguments})"
            ), file=sys.stderr)
