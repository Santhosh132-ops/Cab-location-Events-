import json
import redis
from kafka import KafkaConsumer

# Configuration
KAFKA_BROKER = 'localhost:9092'
TOPIC = 'cab-locations'
GROUP_ID = 'location-consumer-group'
REDIS_HOST = 'localhost'
REDIS_PORT = 6379

def process_messages():
    # Connect to Redis
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        r.ping() # Check connection
        print("Connected to Redis")
    except redis.ConnectionError:
        print("Could not connect to Redis. Is it running?")
        r = None

    print("Waiting for messages...")
    
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
            
            print(f"Received update for {driver_id}: {data}")
            
            # Store in Redis
            if r:
                # Key: driver:{id}, Value: JSON string
                r.set(f"driver:{driver_id}", json.dumps(data))
                # Publish to channel for real-time updates
                r.publish('driver-updates', json.dumps(data))
                
    except KeyboardInterrupt:
        print("Stopping consumer...")
    finally:
        consumer.close()

if __name__ == '__main__':
    process_messages()
