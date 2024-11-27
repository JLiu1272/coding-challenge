from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import redis

app = Flask(__name__)
redis_client = redis.Redis()

"""
Implementing Rate Limiter using Flask Limiter

The purpose is to see how other libraries designed their rate limiter
"""

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="redis://localhost:6379"
)


@app.route("/api/endpoint")
@limiter.limit("10 per minute")
def api_endpoint():
    return jsonify({"message": "Hello, World!"})


if __name__ == "__main__":
    app.run(debug=True)
