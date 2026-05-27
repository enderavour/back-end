# Task BE #4: Add Migrations

Created Models, Pydantic schemas, created and run migrations, added logging 

1. To run the container:
```bash
docker compose up --build 
```

2. To run migrations:
```bash
alembic revision --autogenerate -m "create users table"
```

3. Apply migrations:
```bash
alembic upgrade head
```

4. Check Users table:
```bash
docker compose exec postgres psql -U postgres -d internship
```
And then enter:
```
\d users
```

4. Run the tests 
To run the tests: 
```bash 
docker compose exec app pytest
```

### Notes:
- Alembic uses synchronous PostgreSQL driver (psycopg2)
- Application uses async PostgreSQL driver (asyncpg)
- Logging added for debugging and monitoring
