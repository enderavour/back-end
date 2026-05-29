# Task BE #2: Add Dockerfile

Added Dockerfile and .dockerignore into the project, implemented CORS with two origins 

Run the app:
```
uvicorn app.main:app --reload
```
Run it with: 
```
python -m http.server 3000
```
And open http://localhost:3000/test.html in browser, afterwards open Dev Tools and navigate into JS console. 
There should be response {status_code: 200, detail: 'ok', result: 'working'} or Object with these values. 

To build the Docker image: 
```
docker build -t fastapi-app .
```

To run the docker image:
```
docker run -p 127.0.0.1:8000:8000 fastapi-app 
```

To run the tests inside Docker:
1. Get the image name:
```
docker images
```
There should be image with the similar name: fastapi-app:latest (on my machine)

2. Run the tests (replace fastapi-app:latest with other name if it is different):
```
docker run -e PYTHONPATH=. -it  fastapi-app:latest pytest
```
