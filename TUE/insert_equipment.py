from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["shipyard"]
collection = db["equipment"]

equipment_list = [
    {
        "equipment_name": "Crane-220T",
        "model_number": "CRN-220T",
        "status": "operational",
        "last_maintenance": "2024-03-15"
    },
    {
        "equipment_name": "Welding Robot-X",
        "model_number": "WLD-X100",
        "status": "under maintenance",
        "last_maintenance": "2024-04-01"
    }
]

collection.insert_many(equipment_list)
print("✅ 장비 데이터 삽입 완료")