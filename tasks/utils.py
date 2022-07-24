import subprocess
from functools import cache, partial
from pathlib import Path
from typing import Any

from cookiecutter.main import cookiecutter

run = partial(subprocess.run, check=True)


def create_from_template(
    template: str,
    extra_context: dict[str, Any] | None = None,
) -> None:
    extra_context = extra_context or {}
    root_dir = str(get_root_directory())
    current_dir = str(Path().absolute())
    cookiecutter(
        template=root_dir,
        no_input=True,
        overwrite_if_exists=True,
        directory=template,
        extra_context={
            "path": current_dir,
            **extra_context,
        },
    )


@cache
def get_root_directory() -> Path:
    output = run(["git", "rev-parse", "--show-toplevel"], capture_output=True)
    return Path(output.stdout.decode().strip())  # type: ignore
