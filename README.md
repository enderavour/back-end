# Task BE #5: Add User CRUD Operations

Implemented Updating, Creating, and Deleting of users, as well as getting all users. Added pagination to user rertieval function. 
Added logging for CRUD operations. 

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
To run the tests: 
```bash 
docker compose exec app pytest
```
