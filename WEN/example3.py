from pymongo import MongoClient

# 1. MongoDB 연결
client = MongoClient("mongodb://localhost:27017/")

# 2. 데이터베이스 및 컬렉션 선택
db = client["orders_wendsday"]
collection = db["order"]

# 3. 기존 데이터 초기화 (중복 방지용)
collection.delete_many({})  # 컬렉션 비우기 (선택 사항)

orders = [
    { "order_id": 1, "order_date": "2025-01-05", "amount": 500 },
    { "order_id": 2, "order_date": "2025-01-10", "amount": 400 },
    { "order_id": 3, "order_date": "2025-01-20", "amount": 300 },

    { "order_id": 4, "order_date": "2025-02-01", "amount": 150 },
    { "order_id": 5, "order_date": "2025-02-10", "amount": 200 },

    { "order_id": 6, "order_date": "2025-03-03", "amount": 90 },   # 제외됨 (100 미만)
    { "order_id": 7, "order_date": "2025-03-15", "amount": 120 }
]

# 데이터 삽입
collection.insert_many(orders)

pipeline = [
    { "$match": { "amount": { "$gte": 100 } } },
    {
        "$group": {
            "_id": { "$month": { "$dateFromString": { "dateString": "$order_date" } } },
            "total": { "$sum": "$amount" }
        }
    },
    { "$match": { "total": { "$gt": 1000 } } }
]

result = collection.aggregate(pipeline)
for doc in result:
    print(doc)