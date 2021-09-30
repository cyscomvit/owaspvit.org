FROM python:3.8

LABEL web image

WORKDIR /web

COPY . .

RUN ["pip3", "install", "pipenv"]

RUN ["pipenv", "install"]

CMD pipenv run python3 app.py
