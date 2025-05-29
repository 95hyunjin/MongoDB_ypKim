from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB 연결
client = MongoClient("mongodb://localhost:27017/")
db = client["chart_db"]
collection = db["color_data"]

@app.route("/")
def index():
    return render_template("index5.html")

@app.route("/insert", methods=["GET", "POST"])
def insert():
    if request.method == "POST":
        label = request.form["label"]
        value = float(request.form["value"])
        collection.insert_one({"label": label, "value": value})
        return redirect(url_for("index"))
    return render_template("insert5.html")

@app.route("/chart-data")
def chart_data():
    docs = list(collection.find())
    labels = [doc["label"] for doc in docs]
    values = [doc["value"] for doc in docs]
    return jsonify({"labels": labels, "values": values})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)