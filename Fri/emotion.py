from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from datetime import datetime
from transformers import pipeline

app = Flask(__name__)

# MongoDB 연결
client = MongoClient("mongodb://localhost:27017/")
db = client["sentiment_db"]
collection = db["comments"]

# 감정 분석 모델 (사전학습 BERT)
sentiment_analyzer = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

# 감정 해석 함수
def analyze_sentiment(text):
    result = sentiment_analyzer(text)[0]["label"]
    if result == "1 star": return "very negative"
    elif result == "2 stars": return "negative"
    elif result == "3 stars": return "neutral"
    elif result == "4 stars": return "positive"
    else: return "very positive"

# 감정별 색상 처리
@app.context_processor
def utility():
    def get_color(sentiment):
        return {
            "very negative": "danger",
            "negative": "warning",
            "neutral": "secondary",
            "positive": "primary",
            "very positive": "success"
        }.get(sentiment, "light")
    return dict(get_color=get_color)

# 메인 페이지
@app.route("/")
def index():
    comments = list(collection.find().sort("timestamp", -1))
    return render_template("index4.html", comments=comments)

# 감정 분석 및 저장
@app.route("/analyze", methods=["POST"])
def analyze():
    text = request.json["comment"]
    sentiment = analyze_sentiment(text)
    collection.insert_one({
        "comment": text,
        "sentiment": sentiment,
        "timestamp": datetime.utcnow()
    })
    return jsonify({"status": "ok", "sentiment": sentiment})

# 감정 통계 (Chart.js 용)
@app.route("/stats")
def stats():
    pipeline = [
        {"$group": {"_id": "$sentiment", "count": {"$sum": 1}}}
    ]
    results = list(collection.aggregate(pipeline))

    sentiment_counts = {
        "very negative": 0,
        "negative": 0,
        "neutral": 0,
        "positive": 0,
        "very positive": 0
    }

    for result in results:
        sentiment_counts[result["_id"]] = result["count"]

    return jsonify(sentiment_counts)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)