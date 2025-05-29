from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["school"]
collection = db["students"]

students = [
    {"name": "Alice", "age": 21, "major": "Computer Science"},
    {"name": "Bob", "age": 22, "major": "Economics"},
    {"name": "Charlie", "age": 20, "major": "Mathematics"}
]

collection.insert_many(students)