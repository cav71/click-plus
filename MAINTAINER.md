### Testing

#### Cloning
```shell
git clone https://github.com/cav71/click-plus.git

```


#### TDD
```bash
PYTHONPATH=src py.test -vvs tests
```

#### junit output
(needs pytest-html, pytest-cov)
```bash
PYTHONPATH=src py.test \
   --junitxml=build/junit.xml \
   --html=build/junit.html --self-contained-html \
   --cov=click.plus --cov-report=build/coverage \
   tests
```