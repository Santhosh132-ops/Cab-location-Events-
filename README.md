# Real-Time Cab Location Tracker

A learning project to demonstrate **Kafka**, **AWS**, and **Real-time APIs**.

## Architecture
```mermaid
graph LR
    P[Producer (Driver)] -->|Location Data| K[Kafka (Local)]
    K -->|Stream| C[Consumer]
    K -->|Stream| D[DynamoDB Consumer]
    C -->|Update| R[Redis]
    C -->|Publish| R
    D -->|Store| AWS[AWS DynamoDB]
    API[FastAPI Backend] -->|Subscribe| R
    API -->|WebSocket| UI[Frontend Map]
```

## Prerequisites
1.  **Docker Desktop** (Must be running)
2.  **Python 3.9+**

## Setup

1.  **Start Infrastructure**
    ```bash
    docker-compose up -d
    ```

2.  **Install Dependencies**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    
    pip install -r producer/requirements.txt -r consumer/requirements.txt -r backend/requirements.txt
    ```

## Running the Project

You will need 4 terminal windows:

1.  **Terminal 1: Backend API**
    ```bash
    uvicorn backend.main:app --reload
    ```

2.  **Terminal 2: Consumer**
    ```bash
    python consumer/main.py
    ```

3.  **Terminal 3: Producer (The Driver)**
    ```bash
    python producer/main.py
    ```

4.  **Browser**
    Open `frontend/index.html` in your browser.

## AWS Integration
To save data to AWS DynamoDB instead of just Redis, refer to [aws_setup.md](aws_setup.md).
