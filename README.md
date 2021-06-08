## Working with the development database

To spin up a dockerized version of the database, run the following command

```bash
docker-compose -p cocktail up -d
```

This will read the docker-compose file and expose a postgres container listening on port 5432. If you run
`docker container list --all`, it will show the container running as `cocktail_db_1`. Note that even if you
shutdown your computer, the container will still run on start-up as long as docker is running.

If you want to shut off the container, run the following command.

```bash
docker-compose -p cocktail down
```

## Getting the tables on the database

We place the scripts used to describe changes in the database in the `migrations` folder. The scripts have an `up`
and `down` to describe the actions taken to change the database's schema/state. To run these scripts, use a tool
like `go-migrate`.

## Common Migrate Commands

```bash
set DB_URL=postgres://user:password@localhost:5432/db?sslmode=disable

migrate -path migrations -database %db_url% up
migrate -path migrations -database %db_url% down 1
```