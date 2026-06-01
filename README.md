# Task BE #6: Add Authorization

Developed login/password authentication, /me endpoint, and Auth0 integration. 

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

2. To test JWT Authentication flow manually:
```bash
curl -H "Authorization: Bearer <JWT_TOKEN>" http://localhost:8000/users/auth0/me
```
The app should return dictionary with user data {id, email, username}.

2. To run the tests 
To run the tests: 
```bash 
docker compose exec app pytest
```
