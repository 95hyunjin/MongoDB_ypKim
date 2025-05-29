from pymongo import MongoClient
from datetime import datetime, timedelta

client = MongoClient("mongodb://localhost:27017/")
db = client["business"]
collection = db["sales"]

# 기존 데이터 초기화
collection.delete_many({})

sales = [
{ "region": "Seoul", "amount": 500 },
{ "region": "Seoul", "amount": 700 },
{ "region": "Busan", "amount": 600 }
]

collection.insert_many(sales)

pipeline = [
      {"$group" : {
              "_id" : "$region" , "total_amount" : {"$sum" : "$amount"}}}
]

result = collection.aggregate(pipeline)

for doc in result:
    print(doc)