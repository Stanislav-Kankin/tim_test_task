FROM python:3.11-slim

WORKDIR /app/src

# Установим netcat-openbsd
RUN apt-get update && apt-get install -y netcat-openbsd && apt-get clean

COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY ./src /app/src
COPY ./entrypoint.sh /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
