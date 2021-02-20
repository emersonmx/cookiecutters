import os
import shutil
import sys
import pathlib

dependency_manager = "poetry"
if not shutil.which(dependency_manager):
    print(f"ERROR: {dependency_manager} not found")
    sys.exit(1)

install = {
    "code": "{{ cookiecutter.install_code_tools }}",
    "test": "{{ cookiecutter.install_test_tools }}",
    "debug": "{{ cookiecutter.install_debug_tools }}",
    "tasks": "{{ cookiecutter.install_tasks_tools }}",
}

tools = {
    "code": ["flake8", "mypy", "black", "isort", "jedi", "rope"],
    "test": ["pytest", "coverage"],
    "debug": ["ipdb"],
    "tasks": ["invoke"],
}

init_command = f"{dependency_manager} init -n"
install_command = f"{dependency_manager} add --dev"
format_command = f"{dependency_manager} add --dev"

if install["tasks"] != "y":
    os.remove("tasks.py")

os.system(f"{init_command}")

base_pyproject_data = ""
with open("base_pyproject.toml") as f:
    base_pyproject_data = f.read().strip()
with open("pyproject.toml", "a+") as f:
    if base_pyproject_data:
        f.write("\n" + base_pyproject_data)
os.remove("base_pyproject.toml")

tools_to_install = []
for tool, can_install in install.items():
    if can_install == "y":
        tools_to_install += tools[tool]

if tools_to_install:
    os.system(f"{install_command} {' '.join(tools_to_install)}")
