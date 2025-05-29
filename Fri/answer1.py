from flask import Flask, request, render_template
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer, util
import torch

app = Flask(__name__)

# MongoDB 연결
client = MongoClient("mongodb://localhost:27017/")
db = client["contract_db"]
collection = db["clauses"]

# 한국어 문장 유사도 모델 로딩
model = SentenceTransformer("jhgan/ko-sbert-sts")

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        user_input = request.form["question"]
        user_embedding = model.encode(user_input, convert_to_tensor=True)

        best_score = -1
        best_clause = "관련된 계약 조항을 찾을 수 없습니다."

        for doc in collection.find():
            clause_embedding = model.encode(doc["clause"], convert_to_tensor=True)
            sim = util.cos_sim(user_embedding, clause_embedding).item()
            if sim > best_score:
                best_score = sim
                best_clause = doc["clause"]

        result = best_clause

    return render_template("index6.html", answer=result)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)