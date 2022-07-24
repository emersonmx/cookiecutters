from invoke import Context, task

from ._core import remove_devdeps, update_devdeps


@task
def sync_devdeps(_):
    # type: (Context) -> None
    remove_devdeps()
    update_devdeps()
