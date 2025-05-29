from flask import Flask, render_template, request
from pymongo import MongoClient
import pandas as pd

app = Flask(__name__)

# MongoDB 연결
client = MongoClient("mongodb://localhost:27017/")
db = client["project_log_db"]
collection = db["daily_logs"]

# 엑셀 데이터 삽입 함수
def insert_excel_data():
    df = pd.read_excel("project_management.xlsx")
    collection.delete_many({})
    collection.insert_many(df.to_dict(orient="records"))

@app.route('/', methods=['GET', 'POST'])
def index():
    result = []
    query = {}

    if request.method == 'POST':
        input_date = request.form.get('input_date')
        input_person = request.form.get('input_person')
        input_issue = request.form.get('input_issue')

        if input_date:
            query["일자"] = input_date.strip()
        if input_person:
            query["담당자"] = {"$regex": input_person.strip(), "$options": "i"}
        if input_issue:
            query["주요이슈"] = {"$regex": input_issue.strip(), "$options": "i"}

        result = list(collection.find(query))

    return render_template("index2.html", result=result)

if __name__ == '__main__':
    insert_excel_data()
    app.run(debug=True, host='0.0.0.0', port=5001)