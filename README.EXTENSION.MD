## click.plus.extension
This package allow creating collection of re-usable arguments.

Example:
This define a "myargument" extension providing a --boost flag to any script needing it.

In a module called my_common_args.py:
```python
import click
from   click.plus.extension import api

class MyArguments(api.ExtensionBase):
    def setup(self, fn, arguments):
        fn = click.option("--boost", type=int, default=1)(fn)
        return fn

    def process(self, kwargs, arguments):
        value = kwargs["value"]
        boost = kwargs.pop("boost")
        factor = arguments["factor"]
        kwargs["value"] = value * boost * factor
```

This can be called from each script needed that --boost flag as:
Eg. in by-two.py:
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

```shell
$> by-two.py --boost 3 9
54 (eg. value=9 * boost=3 * factor=2)
```
