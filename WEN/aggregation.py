from pymongo import MongoClient
from pprint import pprint
from datetime import datetime

# MongoDB 연결 및 초기화
client = MongoClient("mongodb://localhost:27017/")
db = client["company"]
employees = db["employees"]
departments = db["departments"]
employees.delete_many({})
departments.delete_many({})

# employees 컬렉션 샘플 데이터
employees.insert_many([
    { "name": "Kim", "age": 35, "salary": 6000, "department": "HR", "birthday": datetime(1989, 4, 10), "tags": ["team", "remote"] },
    { "name": "Lee", "age": 28, "salary": 4800, "department": "HR", "birthday": datetime(1996, 1, 22), "tags": ["solo"] },
    { "name": "Choi", "age": 42, "salary": 7200, "department": "Dev", "birthday": datetime(1982, 12, 5), "tags": ["lead", "on-site"] },
    { "name": "Park", "age": 31, "salary": 5300, "department": "Dev", "birthday": datetime(1993, 7, 8), "tags": ["remote"] },
    { "name": "Yoon", "age": 26, "salary": 3900, "department": "Marketing", "birthday": datetime(1998, 9, 18), "tags": ["event", "remote"] }
])

# departments 컬렉션 샘플 데이터
departments.insert_many([
    { "_id": "HR", "manager": "Director A" },
    { "_id": "Dev", "manager": "Director B" },
    { "_id": "Marketing", "manager": "Director C" }
])

# 파이프라인 실행 예시
pipeline = [
    { "$match": { "age": { "$gt": 30 } } },
    { "$unwind": "$tags" },
    { "$group": { "_id": "$department", "avg_salary": { "$avg": "$salary" } } },
    { "$project": { "department": "$_id", "avg_salary": 1, "_id": 0 } },
    { "$sort": { "avg_salary": -1 } },
    { "$limit": 5 },
    { "$skip": 0 },
    { "$addFields": { "retrieved_at": datetime.now() } },  
    #{ "$count": "total_docs" } 앞의 결과들 다 날라가고 그냥 개수만 남아버림
]

# 하나씩 단계적으로 실행 (예시로 일부 단계 선택적 실행)
# $lookup과 $replaceRoot는 별도 실행
lookup_pipeline = [
    { #loolup자체는 "as"필드에 조인된 데이터를 새로 추가하는 거임 (메인 문서에 조인을 덧 붙인다는 느낌. print에 있는 colliection 뒤에 붙는거임)
        "$lookup": {
            "from": "departments",
            "localField": "department",
            "foreignField": "_id",
            "as": "dept_info"
        }
    },
    { "$unwind": "$dept_info" },
    { "$replaceRoot": { "newRoot": "$dept_info" } } #이렇게 하면 lookup_pipeline의 결과만 나오게 됨
]

# 결과 출력 (예시로 lookup 사용)
print("\n📌 $lookup + $replaceRoot 결과:")
for doc in employees.aggregate(pipeline):
    pprint(doc)
