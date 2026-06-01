# Task BE #6: Add Authorization

Developed login/password authentication, /me endpoint, and Auth0 integration. 

1. To run the container:
```bash
docker compose up --build 
```

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
