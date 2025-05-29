from pymongo import MongoClient
from datetime import datetime, timedelta

client = MongoClient("mongodb://localhost:27017/")
db = client["business_2"]
collection = db["sales"]


one_year_ago = datetime.now() - timedelta(days=365)

sales = [
{ "amount": 1000, "date": "2024-04-05" },
{ "amount": 500,  "date": "2024-04-15" },
{ "amount": 800,  "date": "2024-04-20" },
{ "amount": 700,  "date": "2024-05-03" },
{ "amount": 1300, "date": "2024-05-18" },
{ "amount": 900,  "date": "2024-06-10" },
{ "amount": 600,  "date": "2024-07-04" },
{ "amount": 1000, "date": "2024-07-15" },
{ "amount": 1100, "date": "2024-10-12" },
{ "amount": 950,  "date": "2025-01-09" },
{ "amount": 1200, "date": "2025-01-28" },
{ "amount": 1400, "date": "2025-03-02" }
]

# 문자열 날짜를 datetime으로 변환
for doc in sales:
    doc["date"] = datetime.strptime(doc["date"], "%Y-%m-%d")
    
collection.insert_many(sales)

pipeline = [
    { "$match": { "date": { "$gte": one_year_ago } } },
    {
        "$project": {
            "month": { "$month": "$date" },
            "amount": 1
        }
    },
    {
        "$group": {
            "_id": "$month",
            "avg_monthly_sales": { "$avg": "$amount" }
        }
    }
]

result = collection.aggregate(pipeline)
for doc in result:
    print(doc)