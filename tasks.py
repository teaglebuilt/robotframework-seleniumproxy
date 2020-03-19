from invoke import task
from pathlib import Path
import os
import os.path
import shutil
import glob


CHANGELOG = "CHANGELOG"
filters = ["poc", "new release", "wip", "cleanup", "!nocl"]


def filter_entries(filename):
    buffer = []
    with open(filename) as old_file:
        buffer = old_file.read().split("\n")

    with open(filename, "w") as new_file:
        for line in buffer:
            if not any(bad_word in line.lower() for bad_word in filters):
                new_file.write(line + "\n")


assert Path.cwd() == Path(__file__).parent


@task
def robot(ctx):
    ctx.run("robot -A atest/run_tests.robot")


@task
def unit(ctx):
    ctx.run("nosetests tests")


@task
def lint(ctx):
    ctx.run("flake8")


@task
def docs(ctx):
    ctx.run("python -m robot.libdoc --pythonpath src SeleniumProxy  docs/keywords.html")
    ctx.run("cp docs/keywords.html docs/index.html")


@task
def compileDev(ctx):
    ctx.run("pip-compile --output-file=requirements-dev.txt dependencies/requirements-dev.in")


@task
def compileProd(ctx):
    ctx.run("pip-compile --output-file=requirements.txt dependencies/requirements.in")


@task
def clean(ctx):
    to_be_removed = [
        "reports/",
        "__pycache__/",
        "src/robotframework_seleniumproxy.egg-info/",
        "dist/",
        "*.html",
        "selenium-screenshot-*.png",
        "geckodriver.log",
        "SeleniumProxy.log",
    ]

    for item in to_be_removed:
        if os.path.isdir(item):
            shutil.rmtree(item)
        elif os.path.isfile(item):
            os.remove(item)
        else:
            for filename in glob.glob(item):
                os.remove(filename)


@task
def build(ctx):
    ctx.run("python setup.py sdist")


@task
def changelog(ctx, version=None):
    if version is not None:
        version = "-c {}".format(version)
    else:
        version = ""
    ctx.run("gcg  -x -o {} -O rpm  {}".format(CHANGELOG, version))
    filter_entries(CHANGELOG)


@task
def release(ctx, version=None):
    assert version is not None
    changelog(ctx, version)
    docs(ctx)
    ctx.run("git add docs/* {}".format(CHANGELOG))
    ctx.run("git tag {}".format(version))
    build(ctx)
    ctx.run("git rm -r --cached dist/")
    ctx.run("git add dist/*")
    ctx.run("git commit -m 'New Release {}'".format(version))
