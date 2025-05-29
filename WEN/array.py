from pymongo import MongoClient
from pprint import pprint

# MongoDB 연결 및 컬렉션 초기화
client = MongoClient("mongodb://localhost:27017/")
db = client["library"]
collection = db["articles"]
collection.delete_many({})

# 샘플 데이터 삽입
articles = [
    { "title": "MongoDB Basics", "tags": ["mongodb", "nosql"], "scores": [75, 85, 92] },
    { "title": "Python Guide",   "tags": ["python", "backend"], "scores": [88, 90, 95] },
    { "title": "NoSQL Overview", "tags": ["nosql", "database"], "scores": [60, 70, 80] },
    { "title": "Data Science",   "tags": ["python", "mongodb", "nosql"], "scores": [89, 91, 93] }
]
collection.insert_many(articles)

# $size: 배열 길이 계산
pipeline_size = [
    {
        "$project": {
            "title": 1,
            "tag_count": { "$size": "$tags" }
        }
    }
]
print("\n📌 $size (태그 개수):")
for doc in collection.aggregate(pipeline_size):
    pprint(doc)

# $in: 배열 내 포함 여부
print("\n📌 $in ('mongodb' 태그 포함):")
for doc in collection.find({ "tags": { "$in": ["mongodb"] } }):
    pprint(doc)

# $all: 배열이 모든 값을 포함
print("\n📌 $all ('mongodb'과 'nosql' 모두 포함):")
for doc in collection.find({ "tags": { "$all": ["mongodb", "nosql"] } }):
    pprint(doc)

# $elemMatch: 배열 요소 조건 일치
print("\n📌 $elemMatch (scores 배열 중 80 < score < 90):")
for doc in collection.find({ "scores": { "$elemMatch": { "$gt": 80, "$lt": 90 } } }):
    pprint(doc)