import os
import sys
import logging

from click.plus.extension.api import ExtensionBase


logger = logging.getLogger(__name__)


class Report(ExtensionBase):
    NAME = "report"
    LOGGING_VAR = "application" # the logging can extract application data
                                # from the extra[LOGGING_VAR]
    def setup(self, fn, arguments):
        from time import monotonic
        from functools import wraps
        from click.decorators import pass_context # this workaround is needed
                                                  # only when developing click.plus

        self.log = log = (arguments.get(f"{self.NAME}.log", {})
                          .get("log", logger))

        @pass_context
        @wraps(fn)
        def inner(ctx, *args, **kwargs):
            cwd = os.getcwd()
            t0 = monotonic()
            failed = False
            try:
                return ctx.invoke(fn, *args, **kwargs)
            except KeyboardInterrupt:
                log.info("Script aborted in %.2fs", monotonic()-t0)
                failed = True
            except Exception:
                envdict = {
                    str(k): str(v)
                    for k, v in
                    sorted(os.environ.items(), key=lambda x: str(x[0]).upper())
                }
                log.info("Script run with errors in %.2fs", monotonic()-t0,
                         extra={
                            self.LOGGING_VAR: {
                                        "cwd" : cwd,
                                        "arguments": sys.argv,
                                        "environment": envdict,
                            },
                         }, exc_info=True)
                failed = True
            finally:
                if not failed:
                    log.info("Script completed in %.2fs", monotonic()-t0)
        return inner

    def process(self, kwargs, arguments):
        self.log.info("started script", extra={
            self.LOGGING_VAR: {
                "arguments": sys.argv,
            }
        })


def example():
    # this is a workaround needed
    # only when developing click.plus
    from click.decorators import command, argument
    from click.types import Choice

    from click.plus.extension import configure

    @command()
    @argument("mode", type=Choice(["raise", "run",], case_sensitive=False))
    @configure(["report",])
    def main(mode):
        if mode == "raise":
            raise RuntimeError("triggered exception")
        print("Hello")
    
    logging.basicConfig(level=logging.DEBUG)
    main()


if __name__ == "__main__":
    example()
