# docker/seed

These files build The Market's databases automatically the **first time** you run
`docker compose --profile core up -d`. You don't need to open or edit them.

- `postgres/market.sql.gz`: all tables and data of the `market` database (PostgreSQL)
- `mongo/website_reviews.json.gz` and `mongo/load_reviews.js`: the `website_reviews` collection (MongoDB)

To explore the data, use pgAdmin (http://localhost:5050) and mongo-express (http://localhost:8081).

The data is AI-generated. All people, phone numbers and emails in it are fictional: every phone number is one digit short of a real Jordanian number, and every email uses the reserved example.com, example.net or example.org domains.
