import redis
import json
import random
import time
import os

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)


def generate_order():
    """Generate an order that matches the model's input schema."""
    order = {
        "Customer Status": random.choice([0, 1]),
        "Quantity Ordered": random.randint(1, 20),
        "Total Retail Price for This Order": random.randint(100, 1000),
        "Cost Price Per Unit": random.randint(10, 100),
    }
    return order


def place_order():
    """Continuously generate and place orders onto the Redis queue."""
    try:
        while True:
            order = generate_order()
            redis_client.lpush("order_queue", json.dumps(order))
            print(f"[ORDER PRODUCED]: {order}", flush=True)
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down order producer...")


if __name__ == "__main__":
    place_order()
