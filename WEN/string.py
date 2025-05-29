from pymongo import MongoClient
from pprint import pprint

# MongoDB 연결 및 컬렉션 준비
client = MongoClient("mongodb://localhost:27017/")
db = client["people"]
collection = db["names"]
collection.delete_many({}) #옛날에 실행해서 쌓인 데이터가 계속해서 쌓이니까 초기화하고 사용하려고 추가

# 샘플 데이터 삽입
data = [
    { "first_name": "Kim",  "last_name": "Minsoo", "name": " Kim " },
    { "first_name": "Lee",  "last_name": "Jieun",  "name": "LEE" },
    { "first_name": "Park", "last_name": "Jihwan", "name": "park" }
]
collection.insert_many(data)

# 문자열 연산자 적용 파이프라인
pipeline = [
    {
        "$project": {
            "first_name": 1,
            "last_name": 1,
            "name": 1,
            "full_name": { "$concat": ["$first_name", " ", "$last_name"] },
            "name_substr": { "$substr": ["$name", 0, 3] },
            "name_lower": { "$toLower": "$name" },
            "name_upper": { "$toUpper": "$name" },
            "name_trimmed": { "$trim": { "input": "$name" } }
        }
    }
]

# 결과 출력
for doc in collection.aggregate(pipeline):
    pprint(doc)