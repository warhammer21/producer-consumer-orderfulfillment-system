# Order Fulfillment System with Machine Learning

## Overview
This project is a simple **Order Fulfillment System** implemented using a **Producer-Consumer architecture** with **Redis Queue** as the message broker. It integrates a **Machine Learning model** for order validation and processing. The system demonstrates the use of **asynchronous, decoupled microservices** for robust and scalable order processing.

## Key Components

### 1. Producer Service (Order Creation)
- Accepts incoming orders via **HTTP API**.
- Pushes order data to a **Redis Queue**.
- Decoupled from the processing service – it **does not wait for order processing** to complete.

### 2. Consumer Service (Order Processing with ML Model)
- Listens to the **Redis Queue**.
- Pulls orders from the queue and **feeds them to a Machine Learning model** for validation/prediction.
- Processes and validates orders based on the ML model's output.
- Capable of scaling independently to handle high traffic.

### 3. Redis Queue
- Acts as a **message broker**.
- Buffers incoming orders, allowing the consumer to process them **at its own pace**.
- Ensures **decoupling** between producer and consumer.

### 4. Machine Learning Model (within Consumer Service)
- Flask-based service embedded within the Consumer.
- Evaluates orders (e.g., fraud detection, demand forecasting, or validation).
- Part of the order processing pipeline.

## Architecture Diagram
```
User → [Producer Service (API)] → [Redis Queue] → [Consumer Service + ML Model]
```

## Asynchronous Nature
- The **Producer Service** is **not blocked** by the **Consumer Service**.
- **Producer** pushes an order to the queue and **immediately returns** a response to the client.
- **Consumer** picks orders from the queue independently and **processes them later**.
- This results in **asynchronous, event-driven processing**.

## Benefits of This Approach
- **Decoupling**: Services operate independently.
- **Scalability**: Consumer instances can be scaled based on workload.
- **Fault Tolerance**: Orders remain in the queue if the consumer is down.
- **Load Buffering**: Handles traffic spikes without overwhelming the consumer.
- **ML Integration**: Orders are evaluated by a predictive model, adding intelligence to the system.

## Difference from API Throttling
- **Queueing** buffers and processes tasks asynchronously.
- **API Throttling** limits incoming requests to prevent overload.
- **This project focuses on queuing**, not throttling.

## Technologies Used
- **Python** (FastAPI/Flask for API and ML integration).
- **Redis** (for queueing).
- **Docker & Docker Compose** (for containerization).
- **Flask** (for serving the ML model).

## Running the Project
### Prerequisites
- **Docker** and **Docker Compose** installed.

### Steps
1. Clone the repository.
2. Navigate to the project folder.
3. Run the following command:
    ```bash
    docker compose up --build
    ```

## Best Practices Implemented
- **Separation of Concerns**: Producer and Consumer have distinct responsibilities.
- **Asynchronous Processing**: Queue enables background processing.
- **Fault Tolerance**: Orders are **not lost** if the consumer is down.
- **Scalability**: Consumer can be scaled horizontally.
- **Containerization**: **Docker Compose** for easy setup and environment consistency.
- **Decoupled Design**: Improves resilience and flexibility.
- **ML Model Integration**: Enhances order processing with intelligent evaluation.

## Future Improvements
- **Persistent Queue**: Use Redis persistence features or **RabbitMQ** for more robust message storage.
- **Retry Mechanism**: Implement retries for failed order processing.
- **Monitoring**: Add logging and monitoring for better observability.
- **Error Handling**: Graceful error handling during order processing.
- **Advanced Model Integration**: Upgrade the ML model to handle more complex predictions.

## Conclusion
This project is a foundational example of **asynchronous, event-driven microservices** with **Machine Learning integration** using a **Producer-Consumer pattern** and **Redis Queue**. It can be extended to handle large-scale, real-world order processing systems with intelligent decision-making capabilities.
