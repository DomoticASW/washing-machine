FROM python:3.11-slim

ENV DEVICE_SERVER_PORT=8080
ENV SERVER_PORT=3000

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./src/main/python/main.py" ]