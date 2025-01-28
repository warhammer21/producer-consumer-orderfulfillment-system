import multiprocessing
import time
import random
def order_placer(queue,order_list):
    for order in order_list:
        print(f"Producer: Producing {order}")
        queue.put(order)
def producer_testing(queue, num_items):
    """Producer that generates num_items and puts them into the queue."""
    for i in range(num_items):
        item = f"Task-{i}"
        print(f"Producer: Producing {item}")
        queue.put(item)
        time.sleep(random.uniform(0.1, 0.5))  # Simulate variable production time
    queue.put(None)
## testng
if __name__ == "__main__":
    print('Producer testing start')
    num_items = 10
    order_list = [{'shoes':10},{'books':11},{'notepads':3}]
    queue = multiprocessing.Queue()
    #producer_process = multiprocessing.Process(target=producer_testing, args=(queue, num_items))
    producer_process = multiprocessing.Process(target=order_placer, args=(queue,order_list))
    producer_process.start()
    producer_process.join()


