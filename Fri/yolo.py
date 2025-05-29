from flask import Flask, request, render_template, redirect, url_for
from pymongo import MongoClient
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from PIL import Image
from ultralytics import YOLO

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# MongoDB 연결
client = MongoClient("mongodb://localhost:27017/")
db = client["media_db"]
collection = db["images"]

# YOLOv8n 모델 로딩
model = YOLO("yolov8n.pt")

# 업로드 폴더 생성
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route("/")
def index():
    images = list(collection.find().sort("upload_time", -1))
    return render_template("index2.html", images=images)

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["image"]
    tags = request.form.get("tags", "").split(",")
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # 해상도 및 파일크기
    img = Image.open(filepath)
    width, height = img.size
    size_kb = os.path.getsize(filepath) / 1024

    # YOLOv8n 객체 인식 실행
    results = model(filepath)
    boxes = results[0].boxes
    names = results[0].names

    detected_objects = []
    for box in boxes:
        label = names[int(box.cls)]
        confidence = float(box.conf)
        detected_objects.append({
            "label": label,
            "confidence": round(confidence, 4)
        })

    # MongoDB에 저장
    doc = {
        "filename": filename,
        "resolution": { "width": width, "height": height },
        "tags": [tag.strip() for tag in tags if tag.strip()],
        "upload_time": datetime.utcnow(),
        "file_size_kb": round(size_kb, 2),
        "detected_objects": detected_objects
    }
    collection.insert_one(doc)
    return redirect(url_for("index"))

@app.route("/view/<filename>")
def view(filename):
    doc = collection.find_one({ "filename": filename })
    return render_template("view2.html", doc=doc)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)