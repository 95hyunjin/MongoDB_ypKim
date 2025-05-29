from pymongo import MongoClient
from pprint import pprint
from datetime import datetime

# MongoDB 연결 및 컬렉션 초기화
client = MongoClient("mongodb://localhost:27017/")
db = client["school"]
collection = db["scores"]
collection.delete_many({})

# 샘플 데이터 삽입
collection.insert_many([
    { "student": "Kim", "subject": "Math", "score": 85, "amount": 100, "salary": 3000, "tag": "A", "date": datetime(2024, 4, 1) },
    { "student": "Lee", "subject": "Math", "score": 90, "amount": 200, "salary": 4000, "tag": "B", "date": datetime(2024, 4, 2) },
    { "student": "Park", "subject": "Math", "score": 78, "amount": 150, "salary": 3500, "tag": "A", "date": datetime(2024, 4, 3) },
    { "student": "Choi", "subject": "Science", "score": 92, "amount": 300, "salary": 5000, "tag": "C", "date": datetime(2024, 4, 4) },
    { "student": "Yoon", "subject": "Science", "score": 88, "amount": 250, "salary": 4500, "tag": "B", "date": datetime(2024, 4, 5) }
])

# Aggregation pipeline
pipeline = [
    {
        "$group": {
            "_id": "$subject",
            "total_amount": { "$sum": "$amount" },
            "average_salary": { "$avg": "$salary" },
            "min_score": { "$min": "$score" },
            "max_score": { "$max": "$score" },
            "first_date": { "$first": "$date" },
            "last_date": { "$last": "$date" },
            "all_students": { "$push": "$student" },
            "unique_tags": { "$addToSet": "$tag" }
        }
    }
]

# 결과 출력
for doc in collection.aggregate(pipeline):
    pprint(doc)