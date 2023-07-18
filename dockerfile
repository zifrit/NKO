FROM python:3.11

SHELL ["/bin/bash", "-c"]

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1




RUN pip install --upgrade pip

RUN useradd -rms /bin/bash am && chmod 777 /opt /run #am это имя нового пользователя

WORKDIR /am

RUN mkdir /am/static && mkdir /am/media && chown -R am:am /am && chmod 755 /am

RUN pip install "poetry==1.4.2"
RUN poetry config virtualenvs.create false --local

COPY --chown=yt:yt . .

RUN poetry install


USER am

