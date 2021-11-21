"""Invoke task file"""
from invoke import task
from os import environ
import toml

PYPROJECT_CONFIG = toml.load("pyproject.toml")
VENV = environ.get("VIRTUAL_ENV")


@task
def black(c, overwrite=False):
    """Run black PEP8 formatter

    Args:
        overwrite (bool): Force overwriting files. If False, show diffs instead.
    """
    if overwrite:
        c.run("black .")
    else:
        c.run("black --diff --check .")


@task
def pylint(c):
    """Run pylint linter"""
    c.run(f"pylint {PYPROJECT_CONFIG['project']['name']}")


@task
def test(c, verbose=False):
    """Run pytest tester"""
    opts = []
    if verbose:
        opts.append("-vv")
    c.run("pytest " + " ".join(opts))


@task(black, pylint, test)
def linters(c):
    """Run all linters"""
    pass


@task
def mkdocs(c, all=False):
    """Compile docs"""
    opts = []
    if all:
        opts.append("-a")
    c.run("sphinx-build docs/source docs/build " + " ".join(opts))
