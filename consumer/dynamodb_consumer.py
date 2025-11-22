import json
import boto3
from kafka import KafkaConsumer
from botocore.exceptions import ClientError

# Configuration
KAFKA_BROKER = 'localhost:9092'
TOPIC = 'cab-locations'
GROUP_ID = 'dynamodb-consumer-group'
DYNAMODB_TABLE = 'CabLocations'
REGION = 'us-east-1' # Change to your region

def get_dynamodb_table():
    dynamodb = boto3.resource('dynamodb', region_name=REGION)
    return dynamodb.Table(DYNAMODB_TABLE)

def process_messages():
    try:
        table = get_dynamodb_table()
        print(f"Connected to DynamoDB table: {DYNAMODB_TABLE}")
    except Exception as e:
        print(f"Failed to connect to DynamoDB: {e}")
        return

    print("Waiting for messages to send to AWS...")
    
    # Create Consumer
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=KAFKA_BROKER,
        group_id=GROUP_ID,
        auto_offset_reset='earliest',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    
    try:
        for msg in consumer:
            data = msg.value
            driver_id = data['driver_id']
            
            # DynamoDB requires Decimal for floats, but we can pass strings or use a helper
            item = {
                'DriverId': driver_id,
                'Timestamp': str(data['timestamp']),
                'Latitude': str(data['latitude']),
                'Longitude': str(data['longitude'])
            }
            
            try:
                table.put_item(Item=item)
                print(f"Written to DynamoDB: {driver_id}")
            except ClientError as e:
                print(f"DynamoDB Error: {e}")
                
    except KeyboardInterrupt:
        print("Stopping consumer...")
    finally:
        consumer.close()

if __name__ == '__main__':
    process_messages()
