_OLD_PATH := $(PATH)
VENV_DIR := {{ cookiecutter.venv_path }}
VIRTUAL_ENV := $(PWD)/$(VENV_DIR)
PATH := $(VIRTUAL_ENV)/bin:$(PATH)

.PHONY: setup
{%- if cookiecutter.package_manager == "pip-tools" %}
setup: piptools-sync
{%- elif cookiecutter.package_manager == "pip" %}
setup: pip-install
{%- endif %}

.PHONY: venv
venv: $(VENV_DIR)

$(VENV_DIR):
	PATH="$(_OLD_PATH)" \
	python -m venv $@
{%- if cookiecutter.package_manager == "pip-tools" %}
	python -m pip install pip-tools
		
requirements.txt: venv pyproject.toml
	python -m piptools compile \
		--quiet \
		--generate-hashes \
		-o $@ \
		pyproject.toml

.PHONY: piptools-sync
piptools-sync: venv
	python -m piptools sync requirements.txt
{%- elif cookiecutter.package_manager == "pip" %}

.PHONY: pip-install
pip-install: venv
	pip install -r requirements.txt
{%- endif %}

.PHONY: run
run: venv
	python main.py

.PHONY: clean
clean:
	rm -rf $(VENV_DIR)
