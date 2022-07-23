from invoke import Context


def get_files(c: Context, file: str, exclude: str = "") -> str:
    cmd = f"git ls-files '{file}'"
    if exclude:
        cmd = f"{cmd} | grep -v '{exclude}'"

    return " ".join(c.run(cmd, hide=True).stdout.strip().splitlines())
