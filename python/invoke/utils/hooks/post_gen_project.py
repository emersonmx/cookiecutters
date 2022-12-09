from pathlib import Path


def apply_snippet() -> None:
    snippet_path = Path("_tasks_snippet.py")
    with open(snippet_path) as f:
        snippet = f.readlines()

    tasks_path = Path("tasks.py")
    if tasks_path.exists():
        snippet.pop(0)
    with open(tasks_path, "a") as f:
        f.writelines(snippet)

    snippet_path.unlink()


def main() -> int:
    apply_snippet()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
