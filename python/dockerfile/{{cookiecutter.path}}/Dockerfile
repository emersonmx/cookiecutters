FROM python:{{ cookiecutter.docker_image_tag }} as base

RUN useradd --shell /bin/bash --create-home python

WORKDIR /home/python
USER python

ENV VIRTUAL_ENV=/home/python/venv
RUN python -m venv $VIRTUAL_ENV

ENV PATH=$VIRTUAL_ENV/bin:$PATH \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONOPTIMIZE=1 \
    PYTHONUNBUFFERED=1

RUN mkdir code/
WORKDIR code

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY --chown=python . .

CMD ["python", "main.py"]
