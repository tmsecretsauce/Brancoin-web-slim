FROM python:3.11-slim
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2 \ 
    && apt-get -y install git
RUN mkdir /usr/src/app
WORKDIR /usr/src/app
COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .
ENV PYTHONUNBUFFERED 1
CMD [ "./start.sh" ]