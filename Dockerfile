FROM python:3.11-slim

ENV PORT=8081
ENV SERVER_PORT=
ENV SERVER_DISCOVERY_ADDR="255.255.255.255"
ENV SERVER_DISCOVERY_PORT=30000

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./src/main/python/main.py" ]