FROM python:3.8

LABEL bot image

WORKDIR /bot

COPY . .

RUN ["pip3", "install", "pipenv"]

RUN ["pipenv", "install"]

CMD pipenv run python3 bot.py
