from pymongo import MongoClient
from pprint import pprint

# 1. MongoDB 연결 및 컬렉션 준비
client = MongoClient("mongodb://localhost:27017/")
db = client["testdb"]
collection = db["people"]
collection.delete_many({})  # 기존 데이터 초기화

# 2. 샘플 데이터 삽입
people = [
    { "name": "Kim",   "age": 30 },
    { "name": "Lee",   "age": 25 },
    { "name": "Park",  "age": 35 },
    { "name": "Choi",  "age": 28 },
    { "name": "Jung",  "age": 22 }
]
collection.insert_many(people)

# 3. 논리 연산자별 쿼리 실행

# $and: age가 20 초과 AND 30 미만
print("\n📌 $and (20 < age < 30):")
for doc in collection.find({
    "$and": [
        { "age": { "$gt": 20 } },
        { "age": { "$lt": 30 } }
    ]
}):
    pprint(doc)

# $or: age가 25 또는 name이 "Kim"
print("\n📌 $or (age == 25 OR name == 'Kim'):")
for doc in collection.find({
    "$or": [
        { "age": 25 },
        { "name": "Kim" }
    ]
}):
    pprint(doc)

# $not: age가 30 초과가 아닌 경우 (즉, 30 이하)
print("\n📌 $not (age NOT > 30):")
for doc in collection.find({
    "age": { "$not": { "$gt": 30 } }
}):
    pprint(doc)

# $nor: age가 25도 아니고 name이 "Kim"도 아닌 경우
print("\n📌 $nor (NOT age == 25 AND NOT name == 'Kim'):")
for doc in collection.find({
    "$nor": [
        { "age": 25 },
        { "name": "Kim" }
    ]
}):
    pprint(doc)