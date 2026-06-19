# Task BE #13: Redis Workflow

Implemented a Redis storage for holding quiz responses for 48 hours, wrote tests to check the implemented functionality. 

1. To run the container:
```bash
docker compose up --build 
```
uvicorn app.main:app --reload
```
Run it with: 
```
python -m http.server 3000
```
And open http://localhost:3000/test.html in browser, afterwards open Dev Tools and navigate into JS console. 
There should be response {status_code: 200, detail: 'ok', result: 'working'} or Object with these values. 

2. To run the tests 
```bash 
docker compose exec app pytest
```

### Notes:
- Alembic uses synchronous PostgreSQL driver (psycopg2)
- Application uses async PostgreSQL driver (asyncpg)
- Logging added for debugging and monitoring
