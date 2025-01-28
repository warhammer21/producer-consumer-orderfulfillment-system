import multiprocessing
import time
import random

def producer(queue, num_items):
    """Producer that generates num_items and puts them into the queue."""
    for i in range(num_items):
        item = f"Task-{i}"
        print(f"Producer: Producing {item}")
        queue.put(item)
        time.sleep(random.uniform(0.1, 0.5))  # Simulate variable production time
    queue.put(None)  # Signal to consumers that production is done

def consumer(queue):
    """Consumer that processes items from the queue."""
    while True:
        item = queue.get()
        if item is None:  # Check for termination signal
            print("Consumer: No more items to consume. Exiting.")
            break
        print(f"Consumer: Processing {item}")
        time.sleep(random.uniform(0.5, 1.0))  # Simulate processing time

if __name__ == "__main__":
    num_items = 10
    queue = multiprocessing.Queue()

    # Create producer and consumer processes
    producer_process = multiprocessing.Process(target=producer, args=(queue, num_items))
    consumer_process = multiprocessing.Process(target=consumer, args=(queue,))

    # Start the processes
    producer_process.start()
    consumer_process.start()

    # Wait for the processes to finish
    producer_process.join()
    consumer_process.join()

    print("Main: Producer and Consumer have finished.")
