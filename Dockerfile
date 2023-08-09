FROM python:3.9-slim-buster

WORKDIR /app

# Install curl and gnupg
RUN apt-get update && \
    apt-get install -y curl gnupg && \
    sh -c "curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -" \
    && sh -c "curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list" \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
    && ACCEPT_EULA=Y apt-get install -y mssql-tools18 \
    && apt-get install -y freetds-dev build-essential \
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
