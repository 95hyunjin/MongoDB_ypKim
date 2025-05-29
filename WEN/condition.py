from pymongo import MongoClient
from pprint import pprint

# MongoDB 연결 및 컬렉션 초기화
client = MongoClient("mongodb://localhost:27017/")
db = client["shop"]
collection = db["customers"]
collection.delete_many({})

# 샘플 데이터 삽입
customers = [
    { "name": "Kim", "amount": 1500, "score": 95 },
    { "name": "Lee", "amount": 800, "score": 82 },
    { "name": "Park", "amount": 1100, "score": 76 },
    { "name": "Choi", "amount": 500, "score": 63 },
    { "name": None, "amount": 200, "score": 58 },
    { "amount": 3000, "score": 89 }  # name 필드 없음
]
collection.insert_many(customers)

# 조건 연산자 적용 파이프라인
pipeline = [
    {
        "$project": {
            "name": { "$ifNull": ["$name", "Unknown"] },
            "amount": 1,
            "score": 1,
            "category": {
                "$cond": [
                    { "$gte": ["$amount", 1000] },
                    "VIP",
                    "Normal"
                ]
            },
            "grade": {
                "$switch": {
                    "branches": [
                        { "case": { "$lt": ["$score", 60] }, "then": "F" },
                        { "case": { "$lt": ["$score", 70] }, "then": "D" },
                        { "case": { "$lt": ["$score", 80] }, "then": "C" },
                        { "case": { "$lt": ["$score", 90] }, "then": "B" }
                    ],
                    "default": "A"
                }
            }
        }
    }
]

# 결과 출력
for doc in collection.aggregate(pipeline):
    pprint(doc)