# Price data collector
Gather and saves cryptocurrency prices for different symbols

## Install and usage
+ Install docker in your local environment.
+ You must have a [postgresql](https://www.postgresql.org/) database avaliable to connect and store data.
+ Inside the project folder execute `docker build -t price-collector .` to construct the container.
+ Create a file `env.list` inside the repository with information about how to acess the database in the following format:
```dockerfile
DBPASSWORD=postgres
DBHOST=my-db-us-east-1.rds.amazonaws.com
DBNAME=crypto-prices
DBUSERNAME=admin
```
+ Execute `docker run -ti --env-file env.list price-collector:latest` to run the app.
