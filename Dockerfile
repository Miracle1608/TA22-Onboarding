FROM python:3.9-slim-buster

WORKDIR /app

RUN apt-get update && \
    apt-get install -y freetds-dev build-essential \
                      unixodbc-dev \
                      libgssapi-krb5-2 \
                      libkrb5-dev \
                      libssl-dev \
                      libcrypto++-dev && \
    apt-get clean

COPY requirements.txt .

RUN pip install --trusted-host pypi.python.org -r requirements.txt

COPY . .

EXPOSE 80

ENV FLASK_ENV=development

CMD ["python", "app.py"]