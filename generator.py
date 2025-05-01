# generator.py
import json, random, time, uuid
from datetime import datetime, timezone
from confluent_kafka import Producer

SERVICES = ["auth-service", "payments-service", "catalog-service"]
p = Producer({"bootstrap.servers": "localhost:9092"})

def emit():
    while True:
        record = {
            "id": str(uuid.uuid4()),
            "service": random.choice(SERVICES),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status_code": random.choices(
                [200, 201, 500, 503],
                weights=[0.9, 0.05, 0.03, 0.02]
            )[0],
            "latency_ms": random.randint(50, 800)
        }
        record["error"] = record["status_code"] >= 500
        p.produce("service-telemetry", json.dumps(record).encode())
        p.poll(0)
        time.sleep(0.05)   # ~20 msg/s

if __name__ == "__main__":
    emit()
