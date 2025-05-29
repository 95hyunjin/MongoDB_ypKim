
from flask import Flask, render_template, jsonify
from pymongo import MongoClient
from bson.json_util import dumps  # BSON 데이터를 JSON 형식으로 변환하기 위해 사용

app = Flask(__name__)  # Flask 애플리케이션 생성

# MongoDB 연결 설정
client = MongoClient("mongodb://localhost:27017/")  # 로컬 MongoDB 서버에 연결
db = client["shipyard_db"]                          # 데이터베이스 선택
collection = db["sensor_logs"]                      # 컬렉션 선택 (센서 로그 데이터 저장소)

@app.route("/")  # 루트 URL로 접속 시 실행되는 함수
def index():
    return render_template("index.html")  # index.html 템플릿 렌더링

@app.route("/data/<sensor_type>")  # 특정 센서 타입 데이터를 요청하는 API 엔드포인트
def get_sensor_data(sensor_type):
    # 해당 센서 타입의 데이터를 최신순으로 100개까지 조회
    data = list(collection.find({"type": sensor_type}).sort("timestamp", -1).limit(100))
    return dumps(data)  # JSON 형식으로 반환 (BSON 변환 포함)

# 애플리케이션 시작 지점
if __name__ == "__main__":
    # 디버그 모드로 실행하며, 외부에서 접속 가능하도록 host를 0.0.0.0으로 설정
    app.run(debug=True, host='0.0.0.0', port=5001)