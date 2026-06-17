# Task BE #15: Add Analytics

Created possibility to export data in JSON and CSV formats. Created appropriate role management rules in order to access and export quiz data. Created and run test cases for implemented functionality. 

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
