FROM python:3.7

LABEL MAINTAINER="Sammy Kariuki" version='1.0'

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY Pipfile Pipfile.lock /app/

RUN pip install pipenv && pipenv install --system

