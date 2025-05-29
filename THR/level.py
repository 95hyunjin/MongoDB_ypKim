from pymongo import MongoClient

# MongoDB 접속
client = MongoClient("mongodb://localhost:27017/")
db = client["company"]
collection = db["employees"]

# 초기화 및 데이터 삽입
collection.delete_many({})

employees = [
    { "_id": 1, "name": "CEO",        "manager_id": None, "is_active": True },
    { "_id": 2, "name": "Manager A",  "manager_id": 1,    "is_active": True },
    { "_id": 3, "name": "Manager B",  "manager_id": 1,    "is_active": True },
    { "_id": 4, "name": "Staff A",    "manager_id": 2,    "is_active": True },
    { "_id": 5, "name": "Staff B",    "manager_id": 2,    "is_active": True },
    { "_id": 6, "name": "Staff C",    "manager_id": 3,    "is_active": True },
]

# 데이터 삽입
collection.insert_many(employees)

# 집계 파이프라인
pipeline = [
    { "$match": { "_id": 1 } },
    {
        "$graphLookup": {
            "from": "employees",
            "startWith": "$_id",
            "connectFromField": "_id",
            "connectToField": "manager_id",
            "as": "subordinates",
            "depthField": "level"
        }
    },
    {
        "$project": {
            "name": 1,
            "subordinates": 1
        }
    }
]

# aggregate는 collection에 호출해야 함
result = collection.aggregate(pipeline)

# 출력
print("조직도 (CEO로부터 전체 하위 직원 조회):")
for doc in result:
    print("상위 직원:", doc["name"])
    for sub in sorted(doc.get("subordinates", []), key=lambda x: x["name"]):
        print(f"  레벨 {sub.get('level')}: {sub['name']}")