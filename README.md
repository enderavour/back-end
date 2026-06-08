# Task BE #11: Add Quizzes

Implemented a Quiz system, enabled Owner and Administrator to create unlimited amount of quizzes, ensured that quiz has atleast 2 questions and each questions has two answers, added the possibility for quizzes to accept multiple answers, addes tests to cover implemented functionality. 

1. To run the container:
```bash
docker compose up --build 
```

2. To run the Alembic migrations:
```bash
docker compose exec app alembic revision --autogenerate -m "add company_id to quizzes"
docker compose exec app alembic upgrade head
```

3. To run the tests 
```bash 
docker compose exec app pytest
```
