import redis
import json
import time
import os
import requests

# Environment variables from docker-compose.yml
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
MODEL_SERVICE_URL = os.getenv("MODEL_SERVICE_URL", "http://model-service:5001/predict")

# Setup Redis client
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

MAX_RETRIES = 5
BASE_DELAY = 1  # Initial delay for backoff in seconds


def call_ml_model(order):
    """Send order data to ML model and get prediction."""
    try:
        response = requests.post(MODEL_SERVICE_URL, json=order, timeout=5)
        response.raise_for_status()
        prediction = response.json().get("prediction", [])
        if not prediction:
            raise ValueError("Empty prediction from model")
        return prediction[0]
    except Exception as e:
        raise RuntimeError(f"ML model request failed: {e}")


def fetch_order_with_retry():
    """Fetch orders from Redis with retries and exponential backoff."""
    retries = 0
    while retries < MAX_RETRIES:
        try:
            order_data = redis_client.rpop("order_queue")
            if order_data:
                order = json.loads(order_data)
                return order
            else:
                return None  # No orders in queue
        except redis.exceptions.ConnectionError as e:
            wait_time = BASE_DELAY * (2 ** retries)
            print(f"Redis connection failed. Retrying in {wait_time:.2f}s... [{retries+1}/{MAX_RETRIES}]")
            time.sleep(wait_time)
            retries += 1

    print("Redis connection failed after max retries. Exiting...")
    return None


def process_order(order):
    """
    Process the order by sending it directly to the ML model.
    """
    try:
        print(f"Processing order: {order}")
        prediction = call_ml_model(order)
        print(f"Successfully processed order: {order}. Prediction: {prediction}")
        return True

    except Exception as e:
        print(f"Order processing failed: {e}")
        return False


def main():
    """Main loop for processing orders with retry and fault tolerance."""
    while True:
        order = fetch_order_with_retry()
        if order is None:
            time.sleep(1)
            continue

        retries = 0
        while retries < MAX_RETRIES:
            if process_order(order):
                break
            retries += 1
            wait_time = BASE_DELAY * (2 ** retries)
            print(f"Retrying order processing in {wait_time:.2f}s... [{retries}/{MAX_RETRIES}]")
            time.sleep(wait_time)

        if retries == MAX_RETRIES:
            print(f"Order failed after {MAX_RETRIES} retries. Moving to Dead Letter Queue: {order}")
            redis_client.lpush("dead_letter_queue", json.dumps(order))

        time.sleep(1)  # Prevent CPU overuse


if __name__ == "__main__":
    main()
