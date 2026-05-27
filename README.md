# Task BE #3: Add Database

Added Docker Compose, integrated PostgreSQL/Redis databases, configured volumes in Docker Compose  

1. To run the application:
```bash
docker compose up --build 
```

2. To manually test the PostgreSQL connection: 
```
docker compose exec postgres psql -U postgres -d internship
```
Afterwards, in shell type:
```sql
SELECT 1; 
```
The result should be selected column with 1. 


3. To manually check Redis connection: 
```bash
docker compose exec redis redis-cli
```
Then, in the prompt enter ```PING```
The output should be ```PONG```

4. In order to check Docker image hot reloading: 
Change "detail": "ok" into "detail": "changed" in routers/heatlh.py, and in the output there should be the following logs: 
```bash 
fastapi_app  | WARNING:  StatReload detected changes in 'app/routers/health.py'. Reloading...
fastapi_app  | INFO:     Shutting down
fastapi_app  | INFO:     Waiting for application shutdown.
fastapi_app  | INFO:     Application shutdown complete.
fastapi_app  | INFO:     Finished server process [8]
fastapi_app  | INFO:     Started server process [9]
fastapi_app  | INFO:     Waiting for application startup.
fastapi_app  | INFO:     Application startup complete.
fastapi_app  | WARNING:  StatReload detected changes in 'app/routers/health.py'. Reloading...
fastapi_app  | INFO:     Shutting down 
```

5. Run the tests 
To run the tests: 
```bash 
docker compose exec app pytest
```
