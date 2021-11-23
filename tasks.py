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
    c.run("sphinx-build docs-source docs " + " ".join(opts))


@task
def clean(c, force=False):
    """Cleanup working directory

    Cleanup will skip `private` and `.idea` directories to preserve developer data.
    Without `--force` we print out what to be done but no deletion will happen!
    """
    if force:
        c.run("git clean -d -x -e private -e .idea -f")
    else:
        c.run("git clean -d -x -e private -e .idea -n")


@task(linters)
def build(c):
    """Build wheel and source packages as preparation for pypi deployment

    Consider doing `clean` before running this!
    """
    c.run("flit build")


@task(linters)
def publish(c):
    """Build and publish on PyPi"""
    print("\n", " PUBLISH ".center(80, "-"), "\nPlease run this command:\n")
    print("flit publish --format wheel")
