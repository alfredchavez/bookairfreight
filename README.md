# BookAirFreight Quotation project

Implemented a REST endpoint according to the provided requirements

### Setup
To get the dev containers running you need to use docker compose:
- `docker-compose up -d --build` : this will instanciate a postgres container and a web container for our django project, then run migrations and running the dev server

Then to populate the database we can use a custom command implemented for this project
- `docker-compose exec web python manage.py populate_db`

### Use endpoint
So you can hit the endpoint at port `8000`
- `http://127.0.0.1:8000/v1/quotes`

With a payload like:
```json
{
	"starting_country": "China",
	"destination_country": "USA",
	"boxes": [
		{
			"count": 100,
			"weight_kg": 10,
			"length": 200,
			"width": 20,
			"height": 30
		}
	]
}
```
### Run tests
And to run tests you can use:
- `docker-compose exec web pytest .`