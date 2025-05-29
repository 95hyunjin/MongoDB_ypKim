from pymongo import MongoClient
from datetime import datetime
import pytz
import random
import time

# MongoDB 연결
client = MongoClient("mongodb://localhost:27017/")
db = client["iot_db"]
collection = db["sensor_logs"]

# 한국 시간대 설정
kst = pytz.timezone("Asia/Seoul")

# 디바이스 ID 리스트
device_ids = ["sensor-001", "sensor-002", "sensor-003", "sensor-004", "sensor-005"]

def generate_sensor_data():
    while True:
        # 현재 KST 시간
        kst_now = datetime.now(kst)

        # 무작위 디바이스 선택
        device_id = random.choice(device_ids)

        # 온도값 랜덤 생성 (예: 10.0 ~ 25.0도 사이)
        temperature = round(random.uniform(10.0, 25.0), 2)

        # MongoDB 문서 구성
        document = {
            "device_id": device_id,
            "timestamp": kst_now.astimezone(pytz.utc),  # MongoDB는 UTC 기준 저장
            "value": temperature,
            "unit": "C"
        }

        # MongoDB에 삽입
        collection.insert_one(document)
        print(f"Inserted: {document}")

        # 3초마다 생성
        time.sleep(3)

# 실행
generate_sensor_data()