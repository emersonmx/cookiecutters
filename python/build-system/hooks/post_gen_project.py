from pathlib import Path
from subprocess import CalledProcessError


def apply_snippet() -> None:
    snippet_path = Path("_pyproject_snippet.toml")
    with snippet_path.open() as f:
        snippet = f.readlines()

    pyproject_path = Path("pyproject.toml")
    if pyproject_path.exists():
        snippet.insert(0, "\n")
    with pyproject_path.open(mode="a") as f:
        f.writelines(snippet)

    snippet_path.unlink()


def main() -> int:
    try:
        apply_snippet()
    except CalledProcessError:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
