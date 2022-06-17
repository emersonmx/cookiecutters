FROM python:{{ cookiecutter.docker_image_tag }} as build

WORKDIR /code

RUN python -m venv /code/venv
ENV PATH=/code/venv/bin:$PATH

COPY requirements.txt .
{%- if cookiecutter.require_hashes == "y" %}
RUN pip install --require-hashes -r requirements.txt
{%- else %}
RUN pip install -r requirements.txt
{%- endif %}


FROM python:{{ cookiecutter.docker_image_tag }}

RUN useradd --create-home {{ cookiecutter.app_user }}
USER {{ cookiecutter.app_user }}

WORKDIR /code

COPY --from=build /code/venv /code/venv
COPY . /code

ENV PATH=/code/venv/bin:$PATH \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONOPTIMIZE=1 \
    PYTHONUNBUFFERED=1

CMD ["python", "main.py"]
