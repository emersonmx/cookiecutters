FROM python:{{ cookiecutter.docker_image_tag }} as base

ENV USER=appuser
ENV HOME=/home/$USER
ENV VIRTUAL_ENV=$HOME/venv
ENV PATH=$VIRTUAL_ENV/bin:$PATH \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONOPTIMIZE=1 \
    PYTHONUNBUFFERED=1

RUN useradd --create-home $USER
USER $USER

WORKDIR $HOME


FROM base as build

RUN python -m venv $VIRTUAL_ENV

COPY requirements.txt .
RUN pip install -r requirements.txt


FROM base as app

WORKDIR $HOME/app

COPY --chown=$USER:$USER --from=build $VIRTUAL_ENV $VIRTUAL_ENV
COPY --chown=$USER:$USER . $HOME/app

CMD ["python", "main.py"]
