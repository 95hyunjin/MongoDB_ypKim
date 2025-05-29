from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["flexdb"]
users = db["users"]

# 사용자 1: 기본 정보만
users.insert_one({
    "name": "Alice",
    "email": "alice@example.com"
})

# 사용자 2: SNS 계정 포함
users.insert_one({
    "name": "Bob",
    "email": "bob@example.com",
    "social": {
        "facebook": "bob.fb",
        "linkedin": "bob.li"
    }
})