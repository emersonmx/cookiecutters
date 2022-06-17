FROM python:{{ cookiecutter.docker_image_tag }} as build

WORKDIR /code

RUN python -m venv /code/venv
ENV PATH=/code/venv/bin:$PATH

COPY requirements.txt .
RUN pip install --require-hashes -r requirements.txt


FROM python:{{ cookiecutter.docker_image_tag }}

RUN useradd --create-home appuser
USER appuser

WORKDIR /code

COPY --from=build /code/venv /code/venv
COPY . /code

ENV PATH=/code/venv/bin:$PATH \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONOPTIMIZE=1 \
    PYTHONUNBUFFERED=1

CMD ["python", "main.py"]
