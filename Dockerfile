FROM python:3.8

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy project
COPY . .

# install dependencies

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

COPY ./entrypoint.sh /


ENTRYPOINT ["sh", "/entrypoint.sh"]



