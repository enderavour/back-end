# Task BE #5: Add User CRUD Operations

Implemented Updating, Creating, and Deleting of users, as well as getting all users. Added pagination to user rertieval function. 
Added logging for CRUD operations. 

1. To run the container:
```bash
docker compose up --build 
```

2. To run the tests 
To run the tests: 
```bash 
docker compose exec app pytest
```

### Notes:
- Alembic uses synchronous PostgreSQL driver (psycopg2)
- Application uses async PostgreSQL driver (asyncpg)
- Logging added for debugging and monitoring
