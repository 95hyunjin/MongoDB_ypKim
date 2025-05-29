from pymongo import MongoClient

# 1. MongoDB 연결
client = MongoClient("mongodb://localhost:27017/")

# 2. 데이터베이스 및 컬렉션 선택
db = client["department_exam1"]
collection = db["employees"]

# 3. 기존 데이터 초기화 (중복 방지용)
collection.delete_many({})  # 컬렉션 비우기 (선택 사항)

# 4. 삽입할 직원 데이터
employees = [
{ "name": "Kim", "department": "Welding" },
{ "name": "Lee", "department": "Welding" },
{ "name": "Park", "department": "Welding" },
{ "name": "Choi", "department": "Design" },
{ "name": "Jung", "department": "Design" },
{ "name": "Yoon", "department": "Design" },
{ "name": "Han", "department": "QA" },
{ "name": "Shin", "department": "QA" },
{ "name": "Seo", "department": "QA" },
{ "name": "Kang", "department": "HR" },
{ "name": "Baek", "department": "HR" },
{ "name": "Jin", "department": "Sales" },
{ "name": "Nam", "department": "Sales" }
    ]

# 5. 데이터 삽입
collection.insert_many(employees)

pipeline = [
    { "$group" : {
                 "_id" : "$department", "total_employees" : {"$sum" : 1}
                    }}
]

result = collection.aggregate(pipeline)
for doc in result:
    print(doc)