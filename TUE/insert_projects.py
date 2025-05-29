from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["shipyard"]
collection = db["projects"]

projects = [
    {
        "project_name": "VLCC-2025",
        "client_name": "Hyundai Oilbank",
        "start_date": "2024-01-01",
        "end_date": "2025-12-31"
    },
    {
        "project_name": "LNGC-Alpha",
        "client_name": "SK Gas",
        "start_date": "2023-06-01",
        "end_date": "2024-12-15"
    }
]

collection.insert_many(projects)
print("✅ 선박 프로젝트 데이터 삽입 완료")