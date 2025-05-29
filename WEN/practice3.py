from pymongo import MongoClient

# 1. MongoDB 연결
client = MongoClient("mongodb://localhost:27017/")

# 2. 데이터베이스 및 컬렉션 선택
db = client["department_exam2"]
collection = db["employees"]

# 3. 기존 데이터 초기화 (중복 방지용)
collection.delete_many({})  # 컬렉션 비우기 (선택 사항)

employees = [
    { "name": "Kim", "department": "Welding", "salary": 6000 },
    { "name": "Lee", "department": "Welding", "salary": 5800 },
    { "name": "Park", "department": "Welding", "salary": 4900 },
    
    { "name": "Choi", "department": "Design", "salary": 5200 },
    { "name": "Jung", "department": "Design", "salary": 5100 },
    { "name": "Yoon", "department": "Design", "salary": 5000 },

    { "name": "Han", "department": "QA", "salary": 4500 },
    { "name": "Shin", "department": "QA", "salary": 4700 },
    { "name": "Seo", "department": "QA", "salary": 4600 }
]

collection.insert_many(employees)

pipeline = [
     {"$group" : {
             "_id" : "$department", "max_salary" : {"$max" : "$salary"}, "min_salary" : {"$min" : "$salary"}, "avg_salary" : {"$avg" : "$salary"}}
      }
]

result = collection.aggregate(pipeline)
for doc in result:
     print(doc)