from pymongo import MongoClient
from datetime import datetime
import random
import time

# MongoDB 연결
client = MongoClient("mongodb://localhost:27017/")
db = client["shipyard_db"]
collection = db["sensor_logs"]

sensor_types = [
    "temperature", "humidity", "gas", "gps", "vibration",
    "noise", "dust", "oxygen", "position", "motion"
]

def generate_sensor_data(sensor_type):
    timestamp = datetime.utcnow()

    if sensor_type == "temperature":
        return {
            "sensor_id": f"TEMP_{random.randint(1, 100)}",
            "type": "temperature",
            "timestamp": timestamp,
            "value": round(random.uniform(15.0, 45.0), 2),
            "unit": "C"
        }

    elif sensor_type == "humidity":
        return {
            "sensor_id": f"HUM_{random.randint(1, 100)}",
            "type": "humidity",
            "timestamp": timestamp,
            "humidity": round(random.uniform(30.0, 90.0), 2),
            "unit": "%"
        }

    elif sensor_type == "gas":
        return {
            "sensor_id": f"GAS_{random.randint(1, 100)}",
            "type": "gas",
            "timestamp": timestamp,
            "gas_type": random.choice(["CO", "CO2", "NH3", "CH4"]),
            "ppm": round(random.uniform(100, 1000), 2)
        }

    elif sensor_type == "gps":
        return {
            "sensor_id": f"GPS_{random.randint(1, 100)}",
            "type": "gps",
            "timestamp": timestamp,
            "location": {
                "lat": round(random.uniform(35.0, 38.0), 6),
                "lon": round(random.uniform(126.0, 128.0), 6)
            },
            "altitude": round(random.uniform(0, 100), 2)
        }

    elif sensor_type == "vibration":
        return {
            "sensor_id": f"VIB_{random.randint(1, 100)}",
            "type": "vibration",
            "timestamp": timestamp,
            "accel_x": round(random.uniform(-2, 2), 3),
            "accel_y": round(random.uniform(-2, 2), 3),
            "accel_z": round(random.uniform(-2, 2), 3),
            "unit": "g"
        }

    elif sensor_type == "noise":
        return {
            "sensor_id": f"NOISE_{random.randint(1, 100)}",
            "type": "noise",
            "timestamp": timestamp,
            "db_level": round(random.uniform(50, 120), 1),
            "unit": "dB"
        }

    elif sensor_type == "dust":
        return {
            "sensor_id": f"DUST_{random.randint(1, 100)}",
            "type": "dust",
            "timestamp": timestamp,
            "pm10": round(random.uniform(10, 150), 2),
            "pm2_5": round(random.uniform(5, 100), 2),
            "unit": "µg/m³"
        }

    elif sensor_type == "oxygen":
        return {
            "sensor_id": f"O2_{random.randint(1, 100)}",
            "type": "oxygen",
            "timestamp": timestamp,
            "o2_level": round(random.uniform(10, 21), 2),
            "unit": "%"
        }

    elif sensor_type == "position":
        return {
            "sensor_id": f"UWB_{random.randint(1, 100)}",
            "type": "position",
            "timestamp": timestamp,
            "worker_id": f"W{random.randint(1000, 9999)}",
            "x": round(random.uniform(0, 200), 2),
            "y": round(random.uniform(0, 100), 2),
            "zone": random.choice(["A", "B", "C"])
        }

    elif sensor_type == "motion":
        return {
            "sensor_id": f"IMU_{random.randint(1, 100)}",
            "type": "motion",
            "timestamp": timestamp,
            "tilt_x": round(random.uniform(-90, 90), 2),
            "tilt_y": round(random.uniform(-90, 90), 2),
            "fall_detected": random.choice([True, False])
        }

# 주기적으로 저장 (Ctrl+C로 중지 가능)
print("센서 데이터 MongoDB 저장 시작 (2초마다)...")

try:
    while True:
        sensor_type = random.choice(sensor_types)
        data = generate_sensor_data(sensor_type)
        collection.insert_one(data)
        print(f"저장됨: {data['sensor_id']} - {sensor_type}")
        time.sleep(2)

except KeyboardInterrupt:
    print("\n데이터 저장 중단됨")