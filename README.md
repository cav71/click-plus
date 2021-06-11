# click-plus

### Introduction
This is a click extension package containing few goodies:

  1. **click.plus.extension** -- supports creation of argument groups

#### click.plus.extension example
Creating a simple extension adding an argument to a main:

```python
import click
import click.plus.extension
from   click.plus.extension import api 


class MyArguments(api.ExtensionBase):
    def setup(self, fn, arguments):
        # adds as many click flags/arguments
        fn = click.option("--boost", type=int, default=1)(fn)
        return fn

    def process(self, kwargs, arguments):
        boost = kwargs.pop("boost")
        kwargs["value"] *= boost
        kwargs["value"] *= arguments["factor"]
        return kwargs    

@click.command()
@click.argument("value", type=int)
@click.plus.extension.configure(["myarguments"], factor=2)
def main(value):
    print("Got", value)
    


```


### testing

```bash
PYTHONPATH=src py.test -vvs tests
```
