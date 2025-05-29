from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from pymongo import MongoClient
from bson.objectid import ObjectId
from collections import defaultdict
from datetime import datetime
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

client = MongoClient("mongodb://localhost:27017/")
db = client["shipyard_db"]
parts_collection = db["parts"]

# 재고 누적 흐름 계산
def calculate_stock_flow(parts):
    sorted_parts = sorted(
        parts,
        key=lambda x: datetime.strptime(x.get('inDate') or x.get('outDate'), "%Y-%m-%d")
    )

    stock_by_part = defaultdict(int)
    for part in sorted_parts:
        code = part.get("partCode", "").strip().lower()
        in_q = part.get("inQuantity", 0)
        out_q = part.get("outQuantity", 0)
        status = part.get("status", "")

        if status == "입고확인":
            stock_by_part[code] += in_q
        elif status == "출고확인":
            stock_by_part[code] -= out_q

        part["stock"] = stock_by_part[code]

    return sorted_parts, stock_by_part

@app.route('/')
def index():
    parts = list(parts_collection.find())
    for part in parts:
        part['_id'] = str(part['_id'])

    sorted_parts, stock_dict = calculate_stock_flow(parts)

    chart_dict = {code: qty for code, qty in stock_dict.items()}
    trend_dict = defaultdict(list)
    for part in sorted_parts:
        code = part['partCode']
        date = part.get('inDate') or part.get('outDate')
        net_change = part.get('inQuantity', 0) - part.get('outQuantity', 0)
        if date:
            trend_dict[code].append({"date": date, "quantity": net_change})

    chart_labels = list(chart_dict.keys())
    chart_data = list(chart_dict.values())

    return render_template(
        'index3.html',
        parts=sorted_parts,
        chart_labels=chart_labels,
        chart_data=chart_data,
        line_chart_data=trend_dict,
        stock_dict=stock_dict
    )

@app.route('/register', methods=['POST'])
def register():
    image = request.files['partImage']
    filename = secure_filename(image.filename)
    image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    status = request.form['status']
    quantity = int(request.form['quantity'])

    part = {
        "image": filename,
        "partCode": request.form['partCode'].strip().lower(),
        "partName": request.form['partName'],
        "spec": request.form['spec'],
        "inDate": request.form['inDate'],
        "outDate": request.form['outDate'],
        "inQuantity": quantity if status == '입고확인' else 0,
        "outQuantity": quantity if status == '출고확인' else 0,
        "status": status
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

    sorted_parts, stock_dict = calculate_stock_flow(results)

    chart_dict = {code: qty for code, qty in stock_dict.items()}
    trend_dict = defaultdict(list)
    for part in sorted_parts:
        code = part['partCode']
        date = part.get('inDate') or part.get('outDate')
        net_change = part.get('inQuantity', 0) - part.get('outQuantity', 0)
        if date:
            trend_dict[code].append({"date": date, "quantity": net_change})

    chart_labels = list(chart_dict.keys())
    chart_data = list(chart_dict.values())

    return render_template(
        'index3.html',
        parts=sorted_parts,
        chart_labels=chart_labels,
        chart_data=chart_data,
        line_chart_data=trend_dict,
        stock_dict=stock_dict
    )

@app.route('/edit/<part_id>', methods=['GET'])
def edit(part_id):
    part = parts_collection.find_one({"_id": ObjectId(part_id)})
    part['_id'] = str(part['_id'])
    return render_template('edit3.html', part=part)

@app.route('/update/<part_id>', methods=['POST'])
def update(part_id):
    status = request.form['status']
    quantity = int(request.form['quantity'])

    updated = {
        "partCode": request.form['partCode'].strip().lower(),
        "partName": request.form['partName'],
        "spec": request.form['spec'],
        "inDate": request.form['inDate'],
        "outDate": request.form['outDate'],
        "inQuantity": quantity if status == '입고확인' else 0,
        "outQuantity": quantity if status == '출고확인' else 0,
        "status": status
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5009)