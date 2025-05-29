from pymongo import MongoClient
from pprint import pprint

# 1. MongoDB 연결 및 컬렉션 준비
client = MongoClient("mongodb://localhost:27017/")
db = client["testdb"]
collection = db["people"]
collection.delete_many({})  # 기존 데이터 초기화

# 2. 예제 데이터 삽입
people = [
    { "name": "Kim",   "age": 30, "color": "red" },
    { "name": "Lee",   "age": 25, "color": "blue" },
    { "name": "Park",  "age": 35, "color": "green" },
    { "name": "Choi",  "age": 30, "color": "yellow" },
    { "name": "Jung",  "age": 40, "color": "blue" }
]

collection.insert_many(people)

# 3. 비교 연산자별 테스트 쿼리 실행

print("\n📌 $eq (age == 30):")
for doc in collection.find({ "age": { "$eq": 30 } }):
    print(doc) #print하면 DB내용 한줄로 나오고 pprint하면 입력된 양식대로 줄바꿈해서 표시됨

print("\n📌 $ne (age != 30):")
for doc in collection.find({ "age": { "$ne": 30 } }):
    pprint(doc)

print("\n📌 $gt (age > 30):")
for doc in collection.find({ "age": { "$gt": 30 } }):
    pprint(doc)

print("\n📌 $gte (age >= 30):")
for doc in collection.find({ "age": { "$gte": 30 } }):
    pprint(doc)

print("\n📌 $lt (age < 30):")
for doc in collection.find({ "age": { "$lt": 30 } }):
    pprint(doc)

print("\n📌 $lte (age <= 30):")
for doc in collection.find({ "age": { "$lte": 30 } }):
    pprint(doc)

print("\n📌 $in (color in ['red', 'blue']):")
for doc in collection.find({ "color": { "$in": ["red", "blue"] } }):
    pprint(doc)

print("\n📌 $nin (color not in ['red', 'blue']):")
for doc in collection.find({ "color": { "$nin": ["red", "blue"] } }):
    pprint(doc)