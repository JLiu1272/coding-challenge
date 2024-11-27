# Rate Limiter

This directory implements rate limiter using 2 methods:

1. Implement rate limiter using 3rd party such as [Flask Limiter](https://flask-limiter.readthedocs.io/en/stable/) library
2. Raw dawg implementation of rate limiting

## How to run the flask limiter implementation

1. Run `docker run -d -p 6379:6379 redis` in a terminal. Make sure you have docker installed, and started the docker daemon. This will start the redis server at port 6379
2. At the root of this project, run `python3 rate_limiter/server_flask_ratelimit.py`. This will start the server.
3. Try to hit this endpoint `http://127.0.0.1:5000/api/endpoint` 10 times in less than 1 minute. On the 11th try, you should see 429 Too Many Requests

## How to run the raw implementation of rate limiter

1. Run `docker run -d -p 6379:6379 redis` in a terminal. Make sure you have docker installed, and started the docker daemon. This will start the redis server at port 6379
2. At the root of this project, run `python3 rate_limiter/server.py`. This will start the server.
3. Try to hit this endpoint `http://127.0.0.1:8080/limited` 10 times in less than 1 minute. On the 11th try, you should see 429 Too Many Requests
