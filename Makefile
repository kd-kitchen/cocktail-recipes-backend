.PHONY: start stop

start:
	docker-compose -p cocktail up -d

stop:
	docker-compose -p cocktail down
