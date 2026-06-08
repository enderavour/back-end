# Task BE #10: Add Admin Role

Implemented an Admin role, added permissions of Owner to appoint and remove administrators, implemented endpoints to view the list of administratores in the company. Added test_admin.py to cover the created functionality. 

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
