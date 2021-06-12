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
**click.plus.extension** allows to create click actions/options
groups that can be shared amongst projects.

This is an example of a cli function taking a single int argument,
multiply by factor and (if provided) multiplied by a boost:

```shell
$> example.py --boost 3 9
Got 54 (eg. 9 * 2 * 3)
```
This is the code:
```python
import click
import click.plus.extension

# This can be placed in any module allowing sharing
from   click.plus.extension import api
class MyArguments(api.ExtensionBase):

    # here you can add as many click arguments/options
    def setup(self, fn, arguments):        
        fn = click.option("--boost", type=int, default=1)(fn)
        return fn

    # process applies the decorator arguments to the value click argument
    # then multiply by the boost factor (if provided)
    def process(self, kwargs, arguments):
        kwargs["value"] *= arguments["factor"]

        boost = kwargs.pop("boost")
        kwargs["value"] *= boost


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
