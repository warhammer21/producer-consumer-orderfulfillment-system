import multiprocessing
import time
import random
def order_placer(queue,order_list):
    for order in order_list:
        print(f"Producer: Producing {order}")
        queue.put(order)
def order_consumer(queue):
    while True:
        item = queue.get()
        if item is None:  # Check for termination signal
            print("Consumer: No more items to consume. Exiting.")
            break
        print(f"Consumer: Processing {item}")
## testng
if __name__ == "__main__":
    print('Producer testing start')
    order_list = [{'shoes':10},{'books':11},{'notepads':3}]
    for _ in range(50):  # Generate 1000 entries
        order_list.append({'shoes': random.randint(1, 4)})
        order_list.append({'books': random.randint(1, 4)})
        order_list.append({'notepads': random.randint(1, 4)})
    queue = multiprocessing.Queue()
    #producer_process = multiprocessing.Process(target=producer_testing, args=(queue, num_items))
    producer_process = multiprocessing.Process(target=order_placer, args=(queue,order_list))
    consumer_process = multiprocessing.Process(target=order_consumer, args=(queue,))

    producer_process.start()
    consumer_process.start()

    producer_process.join()
    consumer_process.join()



