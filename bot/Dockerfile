FROM python:3.11-alpine
RUN apk update \
    apk add \
    build-base \
    postgresql \
    postgresql-dev \
    libpq \
    python3-dev \
    gcc \
    libc-dev \
    libffi-dev
RUN mkdir /usr/src/app
WORKDIR /usr/src/app
COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENV PYTHONUNBUFFERED 1
CMD [ "python", "-u" , "./app.py" ]