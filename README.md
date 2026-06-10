# Task BE #12: Quiz Workflow

Developed a quiz workflow, where users can select a company and a quiz, complete them, and be displayed in the profile. Added calculating of average score for a user within a company and across the system. 

1. To run the container:
```bash
docker compose up --build 
```

2. To run the Alembic migrations:
```bash
docker compose exec app alembic upgrade head
```

3. To run the tests 
```bash 
docker compose exec app pytest
```
