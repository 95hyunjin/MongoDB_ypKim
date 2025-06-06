from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

client = MongoClient("mongodb://localhost:27017/")
db = client["shipyard_db1"]
parts_collection = db["parts"]

@app.route('/')
def index():
    parts = list(parts_collection.find())
    for part in parts:
        part['_id'] = str(part['_id'])

    from collections import defaultdict

    chart_dict = defaultdict(int)
    for part in parts:
        key = part['partCode'].strip().lower()
        chart_dict[key] += part['quantity']

    chart_labels = list(chart_dict.keys())
    chart_data = list(chart_dict.values())

    return render_template('index.html', parts=parts, chart_labels=chart_labels, chart_data=chart_data)

@app.route('/register', methods=['POST'])
def register():
    image = request.files['partImage']
    filename = secure_filename(image.filename)
    image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    part = {
        "image": filename,
        "partCode": request.form['partCode'].strip().lower(),  
        "partName": request.form['partName'],
        "spec": request.form['spec'],
        "inDate": request.form['inDate'],
        "outDate": request.form['outDate'],
        "quantity": int(request.form['quantity']),
        "status": request.form['status']
    }
    parts_collection.insert_one(part)
    return redirect(url_for('index'))

@app.route('/search', methods=['POST'])
def search():
    query = {}
    if request.form.get('searchPartCode'):
        query["partCode"] = request.form['searchPartCode'].strip().lower()
    if request.form.get('searchPartName'):
        query["partName"] = request.form['searchPartName']
    if request.form.get('searchSpec'):
        query["spec"] = request.form['searchSpec']
    if request.form.get('searchStatus'):
        query["status"] = request.form['searchStatus']

    results = list(parts_collection.find(query))
    for part in results:
        part['_id'] = str(part['_id'])

    # 차트는 전체 기준
    pipeline = [
        {
            "$group": {
                "_id": "$partCode",
                "totalQuantity": { "$sum": "$quantity" }
            }
        },
        { "$sort": { "_id": 1 } }
    ]
    agg_result = list(parts_collection.aggregate(pipeline))
    chart_labels = [doc['_id'] for doc in agg_result]
    chart_data = [doc['totalQuantity'] for doc in agg_result]

    return render_template('index.html', parts=results, chart_labels=chart_labels, chart_data=chart_data)

@app.route('/edit/<part_id>', methods=['GET'])
def edit(part_id):
    part = parts_collection.find_one({"_id": ObjectId(part_id)})
    part['_id'] = str(part['_id'])
    return render_template('edit.html', part=part)

@app.route('/update/<part_id>', methods=['POST'])
def update(part_id):
    updated = {
        "partCode": request.form['partCode'].strip().lower(),  
        "partName": request.form['partName'],
        "spec": request.form['spec'],
        "inDate": request.form['inDate'],
        "outDate": request.form['outDate'],
        "quantity": int(request.form['quantity']),
        "status": request.form['status']
    }

    if 'partImage' in request.files and request.files['partImage'].filename:
        image = request.files['partImage']
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        updated["image"] = filename

    parts_collection.update_one({"_id": ObjectId(part_id)}, {"$set": updated})
    return redirect(url_for('index'))

@app.route('/delete/<part_id>', methods=['GET'])
def delete(part_id):
    parts_collection.delete_one({"_id": ObjectId(part_id)})
    return redirect(url_for('index'))

# 기존 데이터 일괄 정리 라우트
@app.route('/fix-partcodes')
def fix_partcodes():
    modified = 0
    for doc in parts_collection.find():
        original = doc.get("partCode", "")
        cleaned = original.strip().lower()
        if original != cleaned:
            parts_collection.update_one(
                {"_id": doc["_id"]},
                {"$set": {"partCode": cleaned}}
            )
            modified += 1
    return f"{modified}개의 partCode가 정리되었습니다."

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5010)