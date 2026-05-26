# Task: Setting Up a FastAPI Project Using Best Practices Submission

The application is a default FastAPI application, which return JSON response on main endpoint and run health check on main endpoint path. 

The endpoint returns:
```json
{
  "status_code": 200,
  "detail": "ok",
  "result": "working"
}
```

To start the application:
```
git clone 
cd 
python -m venv venv 
source venv/bin/activate
pip install uvicorn fastapi pytest httpx
uvicorn app.main:app --reload
```

To run the tests:
```
PYTHONPATH=. pytest
```
