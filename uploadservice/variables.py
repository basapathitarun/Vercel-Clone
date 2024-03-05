import redis

# Connect to Redis (adjust host and port if needed)
try:
    publisher = redis.Redis(host='localhost', port=6379)  # Use default port unless specified otherwise
    publisher.ping()  # Check connection health
except redis.exceptions.ConnectionError as e:
    print(f"Failed to connect to Redis: {e}")
    exit(1)  # Exit with error code

# Push to the list (ensure 'id' is defined and has a value)
try:
    id = '123'
    publisher.lpush("build-queue", id)
    print("Value added to list successfully.")
except redis.exceptions.RedisError as e:
    print(f"Error pushing to Redis: {e}")
