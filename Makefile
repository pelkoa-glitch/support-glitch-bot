DC = docker compose
APP = docker_compose/app.yaml
CONSUMER_APP = docker_compose/consumer.yaml
CONSUMER_CONTAINER = bot-faststream
BOT_APP = docker_compose/bot.yaml
BOT_CONTAINER = glitch-bot
EXEC = docker exec -it
LOGS = docker logs
ENV = --env-file .env


.PHONY: all
all:
	${DC} -f ${CONSUMER_APP} ${ENV} -f ${BOT_APP} ${ENV} up --build -d

.PHONY: all-down
all-down:
	${DC} -f ${CONSUMER_APP} ${ENV} -f ${BOT_APP} ${ENV} down

.PHONY: consumer
consumer:
	${DC} -f ${CONSUMER_APP} ${ENV} up --build -d

.PHONY: consumer-logs
consumer-logs:
	${LOGS} -f ${CONSUMER_CONTAINER} -f

.PHONY: consumer-down
consumer-down:
	${DC} -f ${CONSUMER_APP} ${ENV} down



.PHONY: bot
bot:
	${DC} -f ${BOT_APP} ${ENV} up --build -d

.PHONY: bot-logs
bot-logs:
	${LOGS} -f ${BOT_CONTAINER} -f

.PHONY: bot-down
bot-down:
	${DC} -f ${BOT_APP} ${ENV} down
