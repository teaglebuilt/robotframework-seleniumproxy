from invoke import task


@task
def robot(ctx):
    ctx.run("robot -A atest/run_tests.robot")


@task
def lint(ctx):
    ctx.run("flake8")


@task
def docs(ctx):
    ctx.run("python -m robot.libdoc --pythonpath src SeleniumProxy  docs/keywords.html")
    ctx.run("cp docs/keywords.html docs/index.html")
