from pymongo import MongoClient

# 1. MongoDB 연결
client = MongoClient("mongodb://localhost:27017/")

# 2. 데이터베이스 및 컬렉션 선택
db = client["department_exam4"]
collection = db["orders"]

# 3. 기존 데이터 초기화 (중복 방지용)
collection.delete_many({})  # 컬렉션 비우기 (선택 사항)

orders = [
{ "order_date": "2024-01-05", "amount": 450 },
{ "order_date": "2024-01-18", "amount": 700 },
{ "order_date": "2024-02-03", "amount": 120 },
{ "order_date": "2024-02-25", "amount": 350 },
{ "order_date": "2024-03-10", "amount": 500 },
{ "order_date": "2024-03-21", "amount": 800 },
{ "order_date": "2024-04-05", "amount": 90 },
{ "order_date": "2024-04-15", "amount": 150 },
{ "order_date": "2024-05-02", "amount": 1000 },
{ "order_date": "2024-05-18", "amount": 300 },
{ "order_date": "2024-06-09", "amount": 200 },
{ "order_date": "2024-06-22", "amount": 150 },
{ "order_date": "2024-07-01", "amount": 80 },
{ "order_date": "2024-07-12", "amount": 250 },
{ "order_date": "2024-08-14", "amount": 600 },
{ "order_date": "2024-08-28", "amount": 420 },
{ "order_date": "2024-09-05", "amount": 180 },
{ "order_date": "2024-10-03", "amount": 550 },
{ "order_date": "2024-11-11", "amount": 90 },
{ "order_date": "2024-12-30", "amount": 1300 }
]
collection.insert_many(orders)

pipeline = [
     {"$group" : {
                  "_id" : {"$month" : { "$dateFromString" : { "dateString" : "$order_date"}}}, "total" : {"$sum":"$amount"}}
      }
]

result = collection.aggregate(pipeline)
for doc in result:
     print(doc)