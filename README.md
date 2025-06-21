# A Washing-machine emulato
A washing machine simulated device in python for testing DomoticASW
---
## 🚀 Run with Docker

```bash
docker run marcoraggio/domoticasw-washing-machine:latest
```
You can configure the container using environment variables:
```
docker run \
  -e SERVER_PORT=3000 \
  -e DEVICE_SERVER_PORT=8080 \
  marcoraggio/domoticasw-washing-machine:latest
```
