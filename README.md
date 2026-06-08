# Task BE #11: Add Quizzes

Implemented a Quiz system, enabled Owner and Administrator to create unlimited amount of quizzes, ensured that quiz has atleast 2 questions and each questions has two answers, added the possibility for quizzes to accept multiple answers, addes tests to cover implemented functionality. 

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

2. To run the Alembic migrations:
```bash
docker compose exec app alembic revision --autogenerate -m "add company_id to quizzes"
docker compose exec app alembic upgrade head
```

3. To run the tests 
```bash 
docker compose exec app pytest
```
