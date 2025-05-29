from ultralytics import YOLO
from pymongo import MongoClient
from datetime import datetime
import pytz

kst = pytz.timezone('Asia/Seoul')
timestamp = datetime.now(kst).strftime("%Y-%m-%d %H:%M:%S %Z%z")

# MongoDB 연결
client = MongoClient("mongodb://localhost:27017/")
db = client["aa"]
logs_collection = db["bb"]

# 데이터 경로와 설정
data_path = "/home/kimub122620/work/yolov8_dataset/data.yaml"
model_name = "yolov8n.pt"  # 또는 yolov8s.pt, yolov8m.pt

# 모델 초기화
model = YOLO(model_name)

# 학습과 로그 저장
def train_and_log():
    results = model.train(
        data=data_path,
        epochs=1,               
        imgsz=640,
        batch=8,
        project="yolov8_roboflow_run",
        name="exp_mongo",
        exist_ok=True,
        verbose=True
    )

    # 전체 결과를 MongoDB에 저장
    log = {
        "timestamp": timestamp,
        "project": "roboflow_yolo_train",
        "model": model_name,
        "train_args": {
            "epochs": 1,
            "imgsz": 640,
            "batch": 8
        },
        "results": results.results_dict if hasattr(results, "results_dict") else results.__dict__
    }

    logs_collection.insert_one(log)
    print("MongoDB에 전체 학습 결과 저장 완료")

if __name__ == "__main__":
    train_and_log()