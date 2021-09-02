## click.plus Example
Let's group a set of options/arguments we'd like to share across 
click scripts/commands.

First we define in some module (eg. my_common_args.py) one or more classes:
```python
import click
from   click.plus import api

class MyBoost(api.ExtensionBase):
    # if NAME is not defined if will fall back to the class name
    NAME = "booster"

    def setup(self, fn, arguments):
        # here one can add as many click.option/click.argument
        # the argments is a dict taken from the decorator (see below)
        # (remember to wrap the (fn) for each line)

        # we define a --boost option taking an int
        fn = click.option("--boost", type=int, default=1)(fn)
        return fn

    def process(self, kwargs, arguments):
        # before entering the main we modify
        # the kwargs passed to the main. arguments is the same dict as in setup
        
        # the factor is provided by the decorator (see below)
        factor = arguments["factor"]

        # kwargs is the dict arguments main will receive (you can modify it in place)
        value = kwargs["value"]
        # we remove the boost argument so main won't be aware of it
        boost = kwargs.pop("boost")
        kwargs["value"] = value * boost * factor
```

To use this --boost flag:
```python
import click
import click.plus

# we need to import the module containing the classes derived from api.ExtensionBase
import my_common_args

# standard click handling
@click.command()
@click.argument("value", type=int)

# configure takes a list of names (case insensitive) and looks up
# { "factor" : 2 } will be passed as arguments to setup and process
@click.plus.extension.configure(["booster"], factor=2)
def main(value):
    print("Got", value)

if __name__ == "__main__":
    main()
```

This is the usage:
```shell
$> by-two.py --boost 3 9
54 (eg. value=9 * boost=3 * factor=2)
```
