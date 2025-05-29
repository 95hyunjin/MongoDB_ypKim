from pymongo import MongoClient
from datetime import datetime, timedelta

client = MongoClient("mongodb://localhost:27017/")
db = client["business"]
collection = db["sales"]

# 기존 데이터 초기화
collection.delete_many({})

# 기준일: 오늘 기준 최근 1년
one_year_ago = datetime.now() - timedelta(days=365)

# 원본 데이터 (문자열 날짜 → datetime 변환 필요)
raw_sales = [
    { "region": "Seoul", "salesperson": "Kim",   "amount": 500,  "date": "2024-04-05" },
    { "region": "Seoul", "salesperson": "Kim",   "amount": 600,  "date": "2024-04-18" },
    { "region": "Seoul", "salesperson": "Lee",   "amount": 300,  "date": "2024-05-02" },
    { "region": "Seoul", "salesperson": "Lee",   "amount": 800,  "date": "2024-05-28" },
    { "region": "Seoul", "salesperson": "Park",  "amount": 700,  "date": "2024-07-15" },
    { "region": "Seoul", "salesperson": "Park",  "amount": 400,  "date": "2024-07-20" },

    { "region": "Busan", "salesperson": "Choi",  "amount": 300,  "date": "2024-04-03" },
    { "region": "Busan", "salesperson": "Choi",  "amount": 250,  "date": "2024-04-25" },
    { "region": "Busan", "salesperson": "Yoon",  "amount": 600,  "date": "2024-04-30" },
    { "region": "Busan", "salesperson": "Yoon",  "amount": 100,  "date": "2024-05-01" },
    { "region": "Busan", "salesperson": "Yoon",  "amount": 800,  "date": "2024-05-17" },

    { "region": "Incheon", "salesperson": "Jung", "amount": 400,  "date": "2024-06-05" },
    { "region": "Incheon", "salesperson": "Jung", "amount": 300,  "date": "2024-06-17" },
    { "region": "Incheon", "salesperson": "Jung", "amount": 350,  "date": "2024-06-25" },
    { "region": "Incheon", "salesperson": "Seo",  "amount": 200,  "date": "2024-07-02" },
    { "region": "Incheon", "salesperson": "Seo",  "amount": 150,  "date": "2024-07-10" },
    { "region": "Incheon", "salesperson": "Seo",  "amount": 100,  "date": "2024-07-20" },

    { "region": "Daegu", "salesperson": "Min",    "amount": 1000, "date": "2025-01-05" },
    { "region": "Daegu", "salesperson": "Min",    "amount": 50,   "date": "2025-01-15" },
    { "region": "Daegu", "salesperson": "Min",    "amount": 70,   "date": "2025-01-25" }
]

# 문자열 날짜를 datetime으로 변환
sales = []
for doc in raw_sales:
    doc["date"] = datetime.strptime(doc["date"], "%Y-%m-%d")
    sales.append(doc)

# 데이터 삽입
collection.insert_many(sales)

# Aggregation Pipeline
pipeline = [
    {
        "$match": {
            "date": { "$gte": one_year_ago }
        }
    },
    {
        "$project": {
            "region": 1,
            "amount": 1,
            "month": { "$month": "$date" }
        }
    },
    {
        "$group": {
            "_id": { "region": "$region", "month": "$month" },
            "total_sales": { "$sum": "$amount" }
        }
    },
    {
        "$match": {
            "total_sales": { "$gte": 1000 }
        }
    },
    {
        "$sort": {
            "total_sales": -1
        }
    }
]

# 실행 및 출력
result = collection.aggregate(pipeline)

print("📊 지역별 월 매출 합계 (1000 이상, 내림차순 정렬):")
for doc in result:
    print(doc)