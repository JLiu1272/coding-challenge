# Rate Limiter

**Challenge:** https://codingchallenges.fyi/challenges/challenge-rate-limiter/

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

## How the raw rate limiter implementation work

This rate limiter uses the token bucket algorithm to limit the number of requests a client can make within a certain time period.

Here's a step-by-step explanation of how it works:

**Token Bucket Algorithm:**

Each client (identified by their IP address) has a "bucket" that holds a certain number of tokens.
Tokens are added to the bucket at a fixed rate (e.g., 1 token per second).
Each request consumes one token from the bucket.
If the bucket is empty (no tokens left), the request is denied (rate-limited).

**Redis for Storage:**

The state of each client's bucket (number of tokens and the last refill time) is stored in a Redis hash.
Redis is used to ensure that the rate limiting works across multiple instances of the server.

**Token Refill Logic:**

When a request is made, the current time is checked against the last refill time.
The number of new tokens to add is calculated based on the elapsed time and the token rate.
The bucket is refilled with the new tokens, up to the maximum allowed tokens.

**Request Handling:**

If there are tokens available in the bucket, one token is consumed, and the request is allowed.
If there are no tokens left, the request is denied with a "429 Too Many Requests" response.

**Here's how the code works:**

token_bucket(ip):

This function checks and updates the token bucket for the given IP address.
It calculates the elapsed time since the last refill and adds new tokens to the bucket.
If there are tokens available, it consumes one token and allows the request.
If there are no tokens left, it denies the request.
Flask Routes:

`/limited`: This route is rate-limited. It calls token_bucket(ip) to check if the request should be allowed or denied.
`/unlimited`: This route is not rate-limited and always allows the request.
Main Block:

The Flask application is run with debugging enabled, listening on all network interfaces at port 8080.
