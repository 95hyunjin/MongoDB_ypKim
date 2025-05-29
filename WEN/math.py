from pymongo import MongoClient
from pprint import pprint

# MongoDB 연결 및 컬렉션 준비
client = MongoClient("mongodb://localhost:27017/")
db = client["shop"]
collection = db["products"]
collection.delete_many({})

# 샘플 데이터 삽입
products = [
    { "name": "A", "price": 100, "tax": 10, "discount": 20, "quantity": 2, "total": 180, "count": 3, "age": 25 },
    { "name": "B", "price": 200, "tax": 20, "discount": 30, "quantity": 1, "total": 190, "count": 2, "age": 34 },
    { "name": "C", "price": 150, "tax": 15, "discount": 10, "quantity": 3, "total": 435, "count": 5, "age": 41 }
]
collection.insert_many(products)

# Aggregation 파이프라인 구성
pipeline = [
    {
        "$project": {
            "name": 1, #위에 있는 DB내용 그대로 출력해라
            "price": 1, 
            "tax": 1,
            "discount": 1,
            "quantity": 1,
            "total": 1,
            "count": 1,
            "age": 1,
            "price_with_tax": { "$add": ["$price", "$tax"] },
            "price_after_discount": { "$subtract": ["$price", "$discount"] },
            "total_price": { "$multiply": ["$quantity", "$price"] },
            "avg_price": { "$divide": ["$total", "$count"] },
            "age_mod_2": { "$mod": ["$age", 2] }
        }
    }
]

# 결과 출력
for doc in collection.aggregate(pipeline):
    pprint(doc)