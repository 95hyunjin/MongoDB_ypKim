from pymongo import MongoClient
from datetime import datetime, timedelta
one_year_ago = datetime.now() - timedelta(days=365)

client = MongoClient("mongodb://localhost:27017/")
db = client["business"]
collection = db["orders"]

orders = [
    { "customer": "Kim",   "amount": 1200, "date": datetime(2024, 4, 10) },
    { "customer": "Kim",   "amount": 800,  "date": datetime(2024, 6, 12) },
    { "customer": "Lee",   "amount": 300,  "date": datetime(2024, 7, 1) },
    { "customer": "Lee",   "amount": 1000, "date": datetime(2024, 9, 5) },
    { "customer": "Park",  "amount": 2000, "date": datetime(2024, 8, 15) },
    { "customer": "Choi",  "amount": 600,  "date": datetime(2025, 1, 20) },
    { "customer": "Choi",  "amount": 900,  "date": datetime(2025, 2, 2) },
    { "customer": "Jung",  "amount": 3000, "date": datetime(2024, 11, 18) },
    { "customer": "Seo",   "amount": 700,  "date": datetime(2025, 3, 3) },
    { "customer": "Seo",   "amount": 650,  "date": datetime(2024, 12, 12) },
    { "customer": "Yoon",  "amount": 250,  "date": datetime(2024, 6, 30) },
    { "customer": "Yoon",  "amount": 100,  "date": datetime(2024, 5, 20) },
    { "customer": "Min",   "amount": 2000, "date": datetime(2025, 1, 5) },
    { "customer": "Min",   "amount": 500,  "date": datetime(2025, 3, 5) }
]

collection.insert_many(orders)


pipeline = [
       {"$match" : {
                "date" : {"$gte" : one_year_ago}}},
       {"$group" : {
                "_id" : "$customer", "total_amount" : {"$sum" : "$amount"}}},
        {"$sort" : { "total_amount" : -1}},
        {"$limit" : 5}
        ]

result = collection.aggregate(pipeline)

for doc in result:
    print(doc)