from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["shop"]
collection = db["orders"]

orders = [
    {
        "customer_name": "Alice",
        "order_date": "2023-07-10",
        "items": [
            {"product_name": "Keyboard", "quantity": 1},
            {"product_name": "Mouse", "quantity": 2}
        ]
    },
    {
        "customer_name": "Bob",
        "order_date": "2023-07-11",
        "items": [
            {"product_name": "Monitor", "quantity": 1}
        ]
    }
]

collection.insert_many(orders)
print("✅ 주문 데이터 삽입 완료")