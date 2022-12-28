```bash
# To run with docker execute
docker compose up --build -d

# The API will be available at http://localhost:8000/fibonacci

# Example:

curl --request POST 'http://localhost:8000/fibonacci' --header 'Content-Type: application/json' --data-raw '{"n": 5}'

# Running tests
docker exec -it flask bash
pytest tests.py -rA
```