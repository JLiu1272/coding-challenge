import time
from flask import Flask, request, jsonify
import redis

# Initialize Flask and Redis
app = Flask(__name__)
redis_client = redis.StrictRedis(
    host="localhost", port=6379, decode_responses=True)

# Token bucket configuration
MAX_TOKENS = 10  # Bucket capacity
TOKEN_RATE = 1   # Tokens added per second


def token_bucket(ip):
    """
    Implements the token bucket algorithm for rate limiting.
    """
    key = f"bucket:{ip}"
    current_time = time.time()

    # Retrieve bucket state
    bucket = redis_client.hgetall(key)
    last_refill = float(bucket.get("last_refill", current_time))
    tokens = int(bucket.get("tokens", MAX_TOKENS))

    # Calculate the time elapsed since last refill
    elapsed_time = current_time - last_refill
    new_tokens = int(elapsed_time * TOKEN_RATE)
    tokens = min(MAX_TOKENS, tokens + new_tokens)
    last_refill = current_time if new_tokens > 0 else last_refill

    print(f"Elaspsed time: {elapsed_time}")
    print(f"New Tokens: {new_tokens}")
    print(f"Tokens: {tokens}")
    print(f"Last Refill: {last_refill}")

    # Check if a token is available
    if tokens > 0:
        tokens -= 1
        redis_client.hset(
            key,
            mapping={"tokens": tokens, "last_refill": last_refill})
        # Set TTL to avoid stale data
        redis_client.expire(key, MAX_TOKENS // TOKEN_RATE)
        return True  # Request is allowed
    else:
        return False  # Request is rate-limited


@app.route("/limited")
def limited():
    ip = request.remote_addr
    if token_bucket(ip):
        return "Limited, don't overuse me!", 200
    else:
        return jsonify({"error": "Too Many Requests"}), 429


@app.route("/unlimited")
def unlimited():
    return "Unlimited! Let's Go!", 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
