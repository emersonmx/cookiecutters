from pathlib import Path
from subprocess import CalledProcessError


def apply_snippet() -> None:
    snippet_path = Path("_tasks_snippet.py")
    with open(snippet_path, "r") as f:
        task_snippet = f.readlines()

    tasks_path = Path("tasks.py")
    if tasks_path.exists():
        task_snippet.pop(0)
    with open(tasks_path, "a") as f:
        f.writelines(task_snippet)

    snippet_path.unlink()


def main() -> int:
    try:
        apply_snippet()
    except CalledProcessError:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
