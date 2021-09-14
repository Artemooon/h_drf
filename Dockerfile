FROM python:3.8

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN mkdir app/
WORKDIR /app/

# install dependencies

COPY poetry.lock pyproject.toml /app/

RUN pip install --upgrade pip && pip install poetry && poetry config virtualenvs.create false && poetry install

# copy project

COPY games .



#
ENTRYPOINT ["sh", "entrypoint.sh"]



