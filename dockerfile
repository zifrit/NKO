FROM python:3.11

SHELL ["/bin/bash", "-c"]

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN pip install --upgrade pip

WORKDIR /am

RUN mkdir /am/static && mkdir /am/media

RUN pip install poetry
RUN poetry config virtualenvs.create false --local

COPY . .

RUN poetry install
