# Backend Ssr Challenge


 Tecnologías empleadas:

- FastApi
- Docker
- MQTT
- InfluxDB
- MySql


Crear archivo .env en raiz del proyecto, con las siguientes variables:

- DOCKER_INFLUXDB_INIT_TOKEN (Auth token influxb)
- DOCKER_INFLUXDB_INIT_USERNAME (INFLUXDB USER)
- DOCKER_INFLUXDB_INIT_PASSWORD (INFLUXDB PASSWORD)
- DOCKER_INFLUXDB_INIT_ORG (INFLUXDB ORGANIZATION)
- DOCKER_INFLUXDB_INIT_BUCKET (INFLUXDB BUCKET)
- DOCKER_INFLUXDB_INIT_HOST (INFLUXDB IP + PORT POR EJ: 0.0.0.0:8686)
- DOCKER_LOCALHOST_IP (IP LOCALHOST)


Levantar proyecto usando docker-compose up --build


