from invoke import task

@task
def robot(ctx):
    ctx.run("robot -A atest/run_tests.robot")