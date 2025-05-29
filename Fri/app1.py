from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
from pymongo import MongoClient
import mysql.connector
import os
from datetime import datetime
from utils.pcd_parser import parse_pcd

UPLOAD_FOLDER = "static/uploads"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# MongoDB 설정
mongo = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo["pointcloud_db"]
mongo_col = mongo_db["point_data"]

# MariaDB 설정 (mysql.connector 사용)
maria = mysql.connector.connect(
    host="localhost",
    user="kimub122620",
    password="1234",
    database="backend"
)

@app.route("/")
def index():
    return render_template("index1.html")

@app.route("/upload", methods=["POST"])
def upload_pcd():
    file = request.files["pcdfile"]
    device_id = request.form["device_id"]
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # 포인트 파싱
    points = parse_pcd(filepath)

    # MongoDB 저장
    mongo_col.insert_one({
        "device_id": device_id,
        "timestamp": datetime.utcnow(),
        "points": points
    })

    return "업로드 및 저장 완료!"
from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
from pymongo import MongoClient
import mysql.connector
import os
from datetime import datetime
from utils.pcd_parser import parse_pcd

UPLOAD_FOLDER = "static/uploads"
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# MongoDB 연결
mongo = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo["pointcloud_db"]
mongo_col = mongo_db["point_data"]

# MariaDB 연결
maria = mysql.connector.connect(
    host="localhost",
    user="kimub122620",
    password="1234",
    database="backend"
)

@app.route("/")
def index():
    return render_template("index1.html")

@app.route("/upload", methods=["POST"])
def upload_pcd():
    file = request.files["pcdfile"]
    device_id = request.form["device_id"]
    device_name = request.form["device_name"]
    operator_name = request.form["operator_name"]
    project_id = request.form["project_id"]

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # 포인트 클라우드 추출
    points = parse_pcd(filepath)

    # MongoDB 저장
    mongo_col.insert_one({
        "device_id": device_id,
        "timestamp": datetime.utcnow(),
        "points": points
    })

    # MariaDB 장비 정보 저장 (기존 있으면 무시)
    cursor = maria.cursor()
    cursor.execute("SELECT COUNT(*) FROM devices WHERE device_id = %s", (device_id,))
    exists = cursor.fetchone()[0]
    if not exists:
        cursor.execute(
            "INSERT INTO devices (device_id, device_name, operator_name, project_id) VALUES (%s, %s, %s, %s)",
            (device_id, device_name, operator_name, project_id)
        )
        maria.commit()
    cursor.close()

    return "업로드 및 저장 완료!"

@app.route("/data/<device_id>")
def get_data(device_id):
    point_doc = mongo_col.find_one({"device_id": device_id}, {"_id": 0, "points": 1, "timestamp": 1})

    cursor = maria.cursor(dictionary=True)
    cursor.execute("SELECT * FROM devices WHERE device_id = %s", (device_id,))
    meta = cursor.fetchone()
    cursor.close()

    return jsonify({
        "metadata": meta,
        "pointcloud": point_doc
    })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)

@app.route("/data/<device_id>")
def get_data(device_id):
    # MongoDB 조회
    point_doc = mongo_col.find_one(
        {"device_id": device_id},
        {"_id": 0, "timestamp": 1, "points": 1}
    )

    # MariaDB 조회
    cursor = maria.cursor(dictionary=True)
    cursor.execute("SELECT * FROM devices WHERE device_id = %s", (device_id,))
    meta = cursor.fetchone()
    cursor.close()

    return jsonify({
        "metadata": meta,
        "pointcloud": point_doc
    })

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)