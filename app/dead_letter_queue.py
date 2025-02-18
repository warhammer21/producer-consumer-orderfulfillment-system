import redis
import json
import time

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def retry_failed_orders():
    """Retries processing failed orders."""
    while True:
        order_data = redis_client.rpop("dead_letter_queue")
        if order_data:
            order = json.loads(order_data)
            print(f"🔄 Retrying Failed Order: {order}")
            redis_client.lpush("valid_orders", json.dumps(order))  # Re-add to queue

        time.sleep(5)

if __name__ == "__main__":
    retry_failed_orders()
