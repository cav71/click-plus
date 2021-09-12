### Release

#### Betas
You can use maintaner/release.py:
```
./maintaner/release.py micro src/click/plus/__init__.py
git push origin beta/0.0.3
```
Or following the instructions.

0. Start from the master branch version
```bash
git co master
git pull
grep __version__ src/click/plus/__init__.py | python -c 'ask=input(); print(ask.split("\"")[1])'
0.0.2
```

1. update the src/click/plus/__init__.py
```python
__version__ = 0.0.3
```
```bash
git commit -m "release 0.0.3" src/click/plus/__init__.py
```

2. Cretate the new branch:
```bash
git co -b beta/0.0.3
git merge branch
git push origin beta/0.0.3
```


#### Prod
1. tag 
```bash
git tag -m release release/N.M.O
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
