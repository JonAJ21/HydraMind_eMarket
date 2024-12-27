DC = docker-compose
EXEC = docker exec -it
LOGS = docker logs
ENV = --env-file docker-compose/.env
APP_FILE = docker-compose/app.yaml
APP_CONTAINER = payment-service

.PHONY: app
app:
	${DC} -f ${APP_FILE} ${ENV} up --build -d

.PHONY: app-up
app-up:
	${DC} -f ${APP_FILE} ${ENV} up -d

.PHONY: app-down
app-down:
	${DC} -f ${APP_FILE} down

.PHONY: app-shell
app-shell:
	${EXEC} ${APP_CONTAINER} bash

.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f
