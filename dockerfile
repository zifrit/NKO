FROM python:3.11

ENV PYTHONUNBUFFERED=1

WORKDIR /test/dj

RUN pip install --upgrade pip
RUN pip install "poetry==1.4.2"
RUN poetry config virtualenvs.create false --local
COPY poetry.lock poetry.lock
COPY pyproject.toml pyproject.toml
RUN poetry install


COPY . .
