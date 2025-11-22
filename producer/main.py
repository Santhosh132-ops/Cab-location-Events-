import time
import json
import random
import uuid
from kafka import KafkaProducer

# Configuration
KAFKA_BROKER = 'localhost:9092'
TOPIC = 'cab-locations'
DRIVER_ID = str(uuid.uuid4())

def simulate_driver_movement():
    # Start at a random location (e.g., somewhere in San Francisco)
    lat = 37.7749 + random.uniform(-0.01, 0.01)
    lon = -122.4194 + random.uniform(-0.01, 0.01)
    
    # Create Producer
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    
    print(f"Starting driver simulation for ID: {DRIVER_ID}")
    
    try:
        while True:
            # Simulate small movement
            lat += random.uniform(-0.0001, 0.0001)
            lon += random.uniform(-0.0001, 0.0001)
            
            data = {
                'driver_id': DRIVER_ID,
                'latitude': lat,
                'longitude': lon,
                'timestamp': time.time()
            }
            
            # Produce message
            producer.send(TOPIC, data)
            
            print(f"Sent: {data}")
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("Stopping simulation...")
    finally:
        producer.flush()
        producer.close()

if __name__ == '__main__':
    simulate_driver_movement()
