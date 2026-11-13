# The Market: data engineering course

Throughout the semester, you will build the data pipeline for **The Market**, a Jordanian supermarket chain with stores in
Al Rabieh, Khalda, Aqaba and Irbid, plus an online store. This repository is your own copy: you work in it,
commit to it, and submit each lab as a pull request.

**Start here: [LAB-GUIDE.md](LAB-GUIDE.md)** has every step: the first-time setup, how to work on each lab, how to
submit, how to catch up, and troubleshooting.

## What runs on your laptop

| Service | What it is | Open it at |
| --- | --- | --- |
| `market-db` | PostgreSQL: sales from the branch cash registers and the online store | `localhost:5433` (from Python) |
| `mongo` | MongoDB: website reviews | `localhost:27018` (from Python) |
| `pgadmin` | View and query PostgreSQL in the browser | http://localhost:5050 |
| `mongo-express` | View MongoDB in the browser | http://localhost:8081 |

## Repository layout

```
README.md            this page
LAB-GUIDE.md         every step: setup, each lab, submitting, catching up, troubleshooting
docker-compose.yml   the four services: databases and browser tools
.env.example         template for your .env (copy it, set your passwords)
.env                 your real passwords: on your laptop only, never committed
requirements.txt     Python packages for the course (each lab adds its own)
.gitignore           files Git must never commit (like .env)
.gitattributes       keeps line endings the same on Windows and Mac
config/pgadmin/      pgAdmin's ready-made connection to market-db
docker/seed/         builds the databases on first start (don't edit)
scripts/             the environment check (check_env.py)
```

Each lab adds the folders it needs, for example `sql/` for your SQL work.
