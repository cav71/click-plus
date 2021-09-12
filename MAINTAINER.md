### Release

#### Betas
1. Cretae a branch:
```bash
git co -b beta/N.M.O
```

2. Verify src/click/plus/__init__.py has __version__ set to N.M.O

#### Prod
1. tag 
```bash
git tag 
```

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
