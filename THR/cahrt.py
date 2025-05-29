from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB 연결
client = MongoClient("mongodb://localhost:27017/")
db = client["dynamic_db"]

# 하나만 선택해서 주석 해제
#collection = db["collection_a"]  # 구조 A
collection = db["collection_b"]  # 구조 B

# 샘플 데이터 삽입 (초기 1회)
def insert_sample_data():
    if collection.count_documents({}) == 0:
        if collection.name == "collection_a":
            sample_data = [
                {"partCode" : "A1001", "partName": "모터", "quantity": 50, "status": "입고완료", "spec" : "" },
                {"partCode" : "B2002", "partName": "배선", "quantity": 0, "status": "출고완료", "spec" : "" },
                {"partCode" : "C3003", "partName": "", "quantity": 15, "status": "", "spec" : "철제" }
            ]
        elif collection.name == "collection_b":
            sample_data = [
                {"description" : "임시부품", "status": "미입고", "inDate": "2025-04-10", "partCode": "", "image" : "", "outDate" : "", "location" : "", "owner" : "", "lastChecked" : "" },
                {"description" : "", "status": "", "inDate": "", "partCode": "D4004", "image" : "motor.jpg", "outDate" : "2025-04-12", "location" : "", "owner" : "", "lastChecked" : "" },
                {"description" : "", "status": "", "inDate": "", "partCode": "", "image" : "", "outDate" : "", "location" : "창고BA", "owner" : "오기사", "lastChecked" : "2025-04-20" }
            ]
        collection.insert_many(sample_data)

@app.route('/')
def index():
    insert_sample_data()
    docs = list(collection.find())

    all_fields = set()
    for doc in docs:
        all_fields.update(doc.keys())

    if "_id" in all_fields:
        all_fields.remove("_id")

    all_fields = sorted(all_fields)
    all_fields = ["no"] + all_fields

    for i, doc in enumerate(docs, start=1):
        doc["no"] = i
        doc.pop("_id", None)

    return render_template("index1.html", fields=all_fields, docs=docs, collection_name=collection.name)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5010)