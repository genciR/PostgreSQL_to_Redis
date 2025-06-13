# PostgreSQL_to_Redis
# Redis Migration Project

This project demonstrates the migration of a user activity tracking system from a PostgreSQL relational database to a Redis NoSQL database. It includes database setup, data population, data modeling, and a programmatic migration process, fulfilling the requirements of the NoSQL Database Course Project.

## Project Overview
- **Relational Database**: PostgreSQL with tables `users`, `products`, `activities`, and `orders`, populated with 15-20 records each.
- **NoSQL Database**: Redis, chosen for its in-memory performance and key-value model suitability.
- **Migration**: Performed using a Python script (`migrate_to_redis.py`) that transforms and transfers data from PostgreSQL to Redis.

## Setup Instructions
Follow these steps to set up and run the project on your local machine:

1. **Install Prerequisites**:
   - Install Docker Desktop from [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/) to run PostgreSQL and Redis containers.
   - Install Python 3.8+ from [https://www.python.org/](https://www.python.org/) if not already installed.
   - Install Git from [https://git-scm.com/](https://git-scm.com/) for version control.

2. **Clone the Repository**:
   - Open Command Prompt and navigate to your desired directory:
   cd C:\path\to\your\directory
    git clone  https://github.com/genciR/PostgreSQL_to_Redis.git
    cd redis-migration-project


3. **Start Docker Containers**:
- Ensure `docker-compose.yml` is in the directory.
- Start the containers with:

docker-compose up



Verify containers are running with:

docker ps
(You should see `pg-db` and `redis-db`).

4. **Install Python Dependencies**:
- Install required libraries using pip:

pip install psycopg2-binary redis Faker

5. **Populate PostgreSQL**:
- Run the setup script to create tables and populate data:

python setup_postgres.py

- Check the output to confirm success (e.g., "Tables created and data populated successfully!").

6. **Migrate Data to Redis**:
- Run the migration script to transfer data:

python migrate_to_redis.py

- Check the output to verify migration (e.g., "Migrated 20 users to Redis").

7. **Verify Data**:
- Access Redis CLI to inspect data:

docker exec -it redis-db redis-cli
KEYS *
HGETALL user:1
LRANGE user:1:activities 0 -1

- Compare with PostgreSQL data using:

docker exec -it pg-db psql -U postgres -d user_activity -c "SELECT * FROM users LIMIT 5;"

## Dependencies
- **Docker**: For running PostgreSQL and Redis containers.
- **Python Libraries**:
- `psycopg2-binary`: For PostgreSQL database connectivity.
- `redis`: For Redis database connectivity.
- `Faker`: For generating realistic test data.

## Files
- `docker-compose.yml`: Configuration for PostgreSQL and Redis containers.
- `setup_postgres.py`: Python script to create and populate PostgreSQL tables.
- `migrate_to_redis.py`: Python script to migrate data from PostgreSQL to Redis.
- `project_report.txt`: Detailed documentation of the project process and findings.
- `screenshots/`: Folder containing screenshots of database outputs and migration results (subfolders: `postgres`, `redis`).

## Notes
- Ensure the PostgreSQL password (`genci1`) matches your `docker-compose.yml` configuration.
- The project assumes a local Docker environment; adjust host/port settings in scripts if using a remote server.
- Refer to `project_report.txt` for a comprehensive explanation of the design, migration, and justification.

## Contributors
- [`Genc Ristemi-gr29911@seeu.edu.mk`]
