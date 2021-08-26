FROM python:3.8

RUN mkdir app/
WORKDIR /app/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# install dependencies

COPY poetry.lock pyproject.toml /app/

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install

# copy project

COPY . .

#
ENTRYPOINT ["sh", "entrypoint.sh"]



