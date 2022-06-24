FROM python:3.8

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

WORKDIR /app
COPY loop.py .
COPY poetry.lock .
COPY pyproject.toml .
COPY makefile .
COPY nzshm_grid_loc nzshm_grid_loc
COPY resources resources
COPY runner.py .

RUN $HOME/.poetry/bin/poetry install --no-root


CMD ["python", "loop.py"]
