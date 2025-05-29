from pymongo import MongoClient
from pprint import pprint
from datetime import datetime

# MongoDB 연결 및 컬렉션 초기화
client = MongoClient("mongodb://localhost:27017/")
db = client["sales"]
collection = db["orders"]
collection.delete_many({})

# 샘플 데이터 삽입 (문자열과 datetime 형식 포함)
orders = [
    { "order_id": 1, "order_date": datetime(2024, 4, 5), "date": "2024-04-05" },
    { "order_id": 2, "order_date": datetime(2025, 1, 15), "date": "2025-01-15" },
    { "order_id": 3, "order_date": datetime(2024, 12, 30), "date": "2024-12-30" }
]
collection.insert_many(orders)

# 날짜 연산자 적용 파이프라인
pipeline = [
    {
        "$project": {
            "order_id": 1,
            "order_date": 1,
            "date": 1,
            "year": { "$year": "$order_date" },
            "month": { "$month": "$order_date" },
            "day": { "$dayOfMonth": "$order_date" },
            "converted_date": { "$dateFromString": { "dateString": "$date" } },
            "formatted_date": { "$dateToString": { "format": "%Y-%m-%d", "date": "$order_date" } }
        }
    }
]

# 결과 출력
for doc in collection.aggregate(pipeline):
    pprint(doc)