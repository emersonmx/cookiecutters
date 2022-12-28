FROM python:{{ cookiecutter.docker_image_tag }} as base

ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH=$VIRTUAL_ENV/bin:$PATH

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN useradd --shell /bin/bash --create-home python

USER python

RUN mkdir /home/python/code
WORKDIR /home/python/code

COPY --chown=python . .

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONOPTIMIZE=1 \
    PYTHONUNBUFFERED=1

CMD ["python", "main.py"]
