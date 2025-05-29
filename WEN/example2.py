from pymongo import MongoClient

# 1. MongoDB 연결
client = MongoClient("mongodb://localhost:27017/")

# 2. 데이터베이스 및 컬렉션 선택
db = client["project_process"]
collection = db["process"]

# 3. 기존 데이터 초기화 (중복 방지용)
collection.delete_many({})  # 컬렉션 비우기 (선택 사항)

project_steps = [
    { "project_name": "VLCC-2025", "process": "Welding",   "status": "Completed" },
    { "project_name": "VLCC-2025", "process": "Painting",  "status": "Completed" },
    { "project_name": "VLCC-2025", "process": "Testing",   "status": "Completed" },
    { "project_name": "VLCC-2025", "process": "Delivery",  "status": "Pending"   },

    { "project_name": "K-Tanker",  "process": "Welding",   "status": "Completed" },
    { "project_name": "K-Tanker",  "process": "Painting",  "status": "Pending"   },
    { "project_name": "K-Tanker",  "process": "Testing",   "status": "Pending"   },

    { "project_name": "OilRig-A1", "process": "Foundation", "status": "Completed" },
    { "project_name": "OilRig-A1", "process": "Welding",    "status": "Completed" },
    { "project_name": "OilRig-A1", "process": "Drilling",   "status": "Completed" }
]

# 데이터 삽입
collection.insert_many(project_steps)

pipeline = [
     { "$group" : { 
               "_id" : "$project_name", 
               "total_steps" : {"$sum" : 1 }, #count(*)와 동일
               "completed_steps" : {
                           "$sum": {
                                  "$cond" : [ { "$eq" : ["$status", "Completed"] } , 1, 0 ]
                            }
                    }
             }
      },
     { "$match" : {"completed_steps": {"$gt" : 2 }}}
]

result = collection.aggregate(pipeline)
for doc in result:
     print(doc)