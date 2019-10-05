FROM python:3.7-alpine
ENV PYTHONUNBUFFERED 1

RUN apk add --no-cache --virtual .build-deps \
    gcc \
    libffi-dev \
    openssl-dev \
    libpq \
    make \
    musl-dev

RUN apk add --no-cache postgresql-dev python3-dev

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN apk del .build-deps

COPY app .
COPY migrations ./migrations
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app.wsgi:app"]
