from flask import Flask, request, render_template
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer, util
import torch

app = Flask(__name__)

# MongoDB 연결
client = MongoClient("mongodb://localhost:27017/")
db = client["reservation_db"]
collection = db["qa_pairs"]

# KoBERT 기반 STS 모델 (한국어 문장 유사도)
model = SentenceTransformer("jhgan/ko-sbert-sts")



# 질의/응답 데이터 없으면 초기 삽입
def insert_sample_data():
 collection.insert_many([
            { "question": "5월 1일 예약 가능한가요?", "answer": "5월 1일은 18:00, 20:00 두 타임만 예약 가능합니다." },
            { "question": "2명 예약하려면 어떻게 하나요?", "answer": "예약은 성함과 날짜, 시간을 남겨주시면 됩니다." },
            { "question": "예약 취소는 어떻게 하나요?", "answer": "전화로만 예약 취소가 가능합니다." }, 
            { "question": "집은 언제 갈 수 있나요?", "answer": "가고싶을때 가시면 됩니다." }
        ])

insert_sample_data()

@app.route("/", methods=["GET", "POST"])
def index():
    result_answer = None

    if request.method == "POST":
        user_input = request.form["question"]

        # 사용자 질문 임베딩
        question_embedding = model.encode(user_input, convert_to_tensor=True)

        best_score = -1
        best_answer = "적절한 답변을 찾을 수 없습니다."

        for doc in collection.find():
            db_question = doc["question"]
            db_embedding = model.encode(db_question, convert_to_tensor=True)

            # 코사인 유사도 계산
            sim = util.cos_sim(question_embedding, db_embedding).item()
            if sim > best_score:
                best_score = sim
                best_answer = doc["answer"]

        result_answer = best_answer

    return render_template("index5.html", answer=result_answer)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)