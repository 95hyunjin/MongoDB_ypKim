import pandas as pd
from pymongo import MongoClient

# 엑셀 파일 불러오기
df = pd.read_excel("contract_clauses.xlsx")  # 첫 번째 행(A행)이 헤더가 아니라서 skiprows=1로 지정

# 열 이름이 정확히 clause, category인지 확인하고 변경
df.columns = ["clause", "category"]

# MongoDB 연결
client = MongoClient("mongodb://localhost:27017/")
db = client["contract_db"]
collection = db["clauses"]

# 기존 데이터 삭제
collection.delete_many({})

# 데이터 삽입
collection.insert_many(df.to_dict(orient="records"))

print("엑셀 기반 계약 조항 데이터 삽입 완료!")
