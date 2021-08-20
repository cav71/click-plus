# click-plus

### Introduction
This is a work in progress to provide a collection of click extensions.

<dl>
 <dt>click.plus.extension</dt>
 <dd>support for reusable  groups of click arguments/options across scripts.
 </dd>
</dl>

### click.plus.extension example
The use case for this package is to collect and organize common options shared across scripts:
```python
@click.command()
@click.argument("value", type=int)
@click.plus.extension.configure(["my-common-args"], factor=2)
def main(value):
```
The `my-common-args` name is defined somewhere and provides to the main a common group of arguments.
#### Example
Let's say we have a set of (fictional) scripts needing
a common input int argument (`value`) a flag (`--boost`) to multiply the value with:
```shell
.
├── by-ten.py
├── by-two.py
└── my_common_args.py
```

```shell
$> by-two.py --boost 3 9
54 (eg. value=9 * boost=3 * factor=2)

$> by-ten.py --boost 4 2
80 (eg. value=2 * boost=4 * factor=10)
```
The implementation of by-two.py/by-ten.py looks like:
```python
import click
import click.plus.extension

import my_common_args

@click.command()
@click.argument("value", type=int)
@click.plus.extension.configure(["myarguments"], factor=2)
def main(value):
    print("Got", value)

if __name__ == "__main__":
    main()
```

> **_NOTE:_** in the by-ten.py just replace the factor=2 with factor=10

The `my_common_args.py` module contains the "**myarguments**" definition:
```python
import click
from   click.plus.extension import api

class MyArguments(api.ExtensionBase):
    # this is the name used in the extension.configure()
    # otherwise it will fall back to MyArguments 
    NAME = "myarguments" 

    # here you can add as many click arguments/options
    # note the form click.option()(fn) calling style
    def setup(self, fn, arguments):
        fn = click.option("--boost", type=int, default=1)(fn)
        return fn

    # arguments
    #  are the keyword arguments to extension.configure()
    #  (eg. factor=2 or factor=10)
    # kwargs
    #  are the keyword arguments to be fed to main()
    #  you can return a new dict here or alter in place
    def process(self, kwargs, arguments):
        value = kwargs["value"]
        # because boost is popped, it won't reach the main()
        boost = kwargs.pop("boost")
        factor = arguments["factor"]
        kwargs["value"] = value * boost * factor
```

