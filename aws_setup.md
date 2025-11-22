# AWS Setup Instructions

To integrate this project with AWS, follow these steps:

## 1. AWS Account & CLI
1.  Ensure you have an AWS Account (Free Tier is sufficient).
2.  Install the **AWS CLI** on your machine.
3.  Run `aws configure` and enter your:
    - Access Key ID
    - Secret Access Key
    - Region (e.g., `us-east-1`)
    - Output format (json)

## 2. Create DynamoDB Table
1.  Go to the AWS Console -> DynamoDB.
2.  Click **Create Table**.
3.  **Table Name**: `CabLocations`
4.  **Partition Key**: `DriverId` (String)
5.  **Sort Key**: `Timestamp` (String)
6.  Use default settings and click **Create table**.

## 3. Install Dependencies
You need `boto3` to interact with AWS.
```bash
pip install boto3
```

## 4. Run the Consumer
Run the special DynamoDB consumer script:
```bash
python consumer/dynamodb_consumer.py
```

Now, when you run the `producer/main.py`, the data will flow:
**Producer -> Kafka (Local) -> Consumer -> AWS DynamoDB**
