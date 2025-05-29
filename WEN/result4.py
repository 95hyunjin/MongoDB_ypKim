from pymongo import MongoClient
from datetime import datetime, timedelta

client = MongoClient("mongodb://localhost:27017/")
db = client["business_2"]
collection = db["sales"]

collection.delete_many({})

sales = [
# Completed
    { "status": "Completed", "amount": 1200 },
    { "status": "Completed", "amount": 800 },
    { "status": "Completed", "amount": 1500 },
    { "status": "Completed", "amount": 1000 },

    # Pending
    { "status": "Pending", "amount": 500 },
    { "status": "Pending", "amount": 700 },
    { "status": "Pending", "amount": 1200 },

    # Cancelled
    { "status": "Cancelled", "amount": 900 },
    { "status": "Cancelled", "amount": 1100 },
    { "status": "Cancelled", "amount": 1300 }]

collection.insert_many(sales)

pipeline = [
        {"$group" : {
                   "_id" : "$status",
                   "total_orders" : {"$sum" : 1},
                    "high_amount" : {"$sum" : {"$cond" : [{"$gte" : ["$amount", 1000]},1,0]}}}},
        {"$project" : {
               "high_ratio" : {
                   "$divide" : ["$high_amount", "$total_orders"]}}}
]

result = collection.aggregate(pipeline)

for doc in result:
    print(doc)