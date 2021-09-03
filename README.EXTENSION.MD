## click.plus Example
In this example we're going to create a set of options/arguments
that can be shared across script and commands.
The script is a click script with two commands, and they both take a common flag `--boost`.
```bash
./hello.py per10 --boost 3 12
Got 360 # 10 * 3 * 12
./hello.py per20 --boost 3 12
Got 720 # 20 * 3 * 12
```

### how to use the options/arguments set
This is the main script (for details on what's in my_common_args please see below)

```python
import click
import click.plus

# That's the module containing the MyBoost api.ExtensionBase derived class
import my_common_args

@click.group()
def main():
    pass

@main.command()
@click.plus.extension.configure(["booster"], factor=10)
@click.argument("value", type=int)
def per10(value)
    print("Got", value)

@main.command()
@click.plus.extension.configure(["booster"], factor=20)
@click.argument("value", type=int)
def per20(value):
    print("Got", value)

if __name__ == "__main__":
    main()
```

### define the options/arguments set
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


This is the usage:
```shell
$> by-two.py --boost 3 9
54 (eg. value=9 * boost=3 * factor=2)
```
