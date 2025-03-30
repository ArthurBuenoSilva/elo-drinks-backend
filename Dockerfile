FROM python:3.13

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /code

RUN apt-get update && apt-get install -y \
    curl iputils-ping postgresql-client nano procps \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /code/

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY ./code /code
