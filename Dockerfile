FROM python:3.11-slim

ENV PORT=8081
ENV SERVER_ADDRESS=
ENV SERVER_DISCOVERY_ADDR="255.255.255.255"
ENV SERVER_DISCOVERY_PORT=30000
ENV ID="WSH001"
ENV NAME="Washing Machine 001"

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./src/main/python/main.py" ]