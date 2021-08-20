# click-plus

### Introduction
This is a curated collection of click extensions.

<dl>
 <dt>click.plus.extension</dt>
 <dd>supports creation of shareable, pre-configured groups of
  click arguments/options.
 </dd>
</dl>

### click.plus.extension example
This click-plus package allows creation of common
groups of click actions/options amongst scritps.

Let's say we have a set of (fictional) scripts needing 
a common input int argument (value) a flag (--boost) to multiply the value with;
moreover the value*boost should be multiplied by a factor parameter script depended.
This is what the scripts look like:

```shell
$> by-two.py --boost 3 9
54 (eg. value=9 * boost=3 * factor=2)

$> by-ten.py --boost 4 2
80 (eg. value=2 * boost=4 * factor=10)
```

The body of by-two.py/by-ten.py looks like:
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

The my_common_args.py module contains the "*myarguments*" definition:
```python
import click
from   click.plus.extension import api

class MyArguments(api.ExtensionBase):
    NAME = "myarguments"
    
    # here you can add as many click arguments/options
    def setup(self, fn, arguments):
        fn = click.option("--boost", type=int, default=1)(fn)
        return fn
    
    # kwargs contains the main **kwargs, you can modify in place
    # or return a new dict here. arguments is a dict to the
    # decorator arguments
    def process(self, kwargs, arguments):
        value = kwargs["value"]
        boost = kwargs.pop("boost")
        factor = arguments["factor"]
        kwargs["value"] = value * boost * factor
```
