import pandas as pd
from pymongo import MongoClient

# 1. 엑셀 파일 로딩
excel_path = "project_management.xlsx"  # 엑셀 파일명 (같은 경로에 있어야 함)
df = pd.read_excel(excel_path)

# 2. MongoDB 연결
client = MongoClient("mongodb://localhost:27017/")
db = client["project_log_db"]
collection = db["daily_logs"]

# 3. 기존 데이터 삭제 후 엑셀 데이터 삽입
collection.delete_many({})
collection.insert_many(df.to_dict(orient="records"))
print("엑셀 데이터 MongoDB에 삽입 완료\n")

# 4. 사용자 입력으로 날짜별 로그 조회
input_date = input("조회할 날짜를 입력하세요 (예: 2025-03-10): ").strip()

# 5. MongoDB에서 해당 날짜 조회
results = list(collection.find({"일자": input_date}))

# 6. 출력
if results:
    print(f"\n{input_date}의 프로젝트 로그:")
    for doc in results:
        print(f"- 담당자: {doc.get('담당자')}")
        print(f"  주요업무: {doc.get('주요업무')}")
        print(f"  주요이슈: {doc.get('주요이슈')}")
        print(f"  비고: {doc.get('비고')}\n")
else:
    print(f"❗ {input_date}에 해당하는 로그가 없습니다.")