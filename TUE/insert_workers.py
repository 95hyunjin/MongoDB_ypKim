from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["shipyard"]
collection = db["workers"]

workers = [
    {
        "name": "Kim Jinho",
        "department": "Welding",
        "shift": "Night",
        "work_logs": [
            {"date": "2024-04-01", "work_hours": 10},
            {"date": "2024-04-02", "work_hours": 8}
        ]
    },
    {
        "name": "Lee Sujin",
        "department": "Painting",
        "shift": "Day",
        "work_logs": [
            {"date": "2024-04-01", "work_hours": 9}
        ]
    }
]

collection.insert_many(workers)
print("✅ 작업자 및 근무 기록 데이터 삽입 완료")