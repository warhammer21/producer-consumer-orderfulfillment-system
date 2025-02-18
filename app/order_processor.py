import redis
import json
#import joblib
import random
import time

# # Load pre-trained ML models
# fraud_model = joblib.load("fraud_detection.pkl")
# delivery_model = joblib.load("delivery_time_estimator.pkl")
#
# redis_client = redis.Redis(host='localhost', port=6379, db=0)
#
# def process_orders():
#     """Fetches orders, runs ML models, and pushes valid orders forward."""
#     while True:
#         order_data = redis_client.rpop("order_queue")
#         if order_data:
#             order = json.loads(order_data)
#             features = [[order["items"]["shoes"], order["items"]["books"]]]
#             fraud_prediction = fraud_model.predict(features)[0]
#
#             if fraud_prediction == 1:
#                 print(f"🚨 Fraud Detected: {order}")
#                 redis_client.lpush("dead_letter_queue", json.dumps(order))  # Send to DLQ
#                 continue  # Skip fraudulent orders
#
#             delivery_time = delivery_model.predict(features)[0]
#             order["delivery_time"] = delivery_time
#             redis_client.lpush("valid_orders", json.dumps(order))
#             print(f"✅ Order Passed ML Checks: {order}")
#
#         time.sleep(1)  # Simulate processing time
#
# if __name__ == "__main__":
#     process_orders()

# Connect to Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Simulate placing an order
order = {"order_id": 123, "items": {"shoes": 2, "books": 3}}
redis_client.lpush("order_queue", json.dumps(order))
print("Order pushed to Redis")

# Simulate consuming an order
order_data = redis_client.rpop("order_queue")
if order_data:
    order = json.loads(order_data)
    print(f"Order consumed: {order}")





