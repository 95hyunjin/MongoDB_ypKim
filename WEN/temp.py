from flask import Flask, render_template, jsonify
from pymongo import MongoClient
from datetime import datetime, timedelta
import pytz

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
db = client["iot_db"]
collection = db["sensor_logs"]

KST = pytz.timezone("Asia/Seoul")

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/data')
def get_data():
    # 최근 3초 이내 데이터만 반환
    three_seconds_ago = datetime.utcnow() - timedelta(seconds=5)

    pipeline = [
        {"$match": {"timestamp": {"$gte": three_seconds_ago}}},
        {"$group": {
            "_id": {
                "device": "$device_id"
            },
            "latest_temp": { "$avg": "$value" }
        }}
    ]

    result = list(collection.aggregate(pipeline))
    data_by_device = {}
    now_kst = datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(KST)
    time_label = now_kst.strftime("%H:%M:%S")

    for doc in result:
        device = doc['_id']['device']
        temp = round(doc['latest_temp'], 2)
        data_by_device[device] = {
            "label": time_label,
            "value": temp
        }

    return jsonify(data_by_device)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)