from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

client = MongoClient("mongodb://localhost:27017/")
db = client["shipyard_db"]
parts_collection = db["parts"]

@app.route('/')
def index():
    parts = list(parts_collection.find())
    for part in parts:
        part['_id'] = str(part['_id'])  
    return render_template('index.html', parts=parts)

@app.route('/register', methods=['POST'])
def register():
    image = request.files['partImage']
    filename = secure_filename(image.filename)
    image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    part = {
        "image": filename,
        "partCode": request.form['partCode'],
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
    if request.form['searchPartCode']:
        query["partCode"] = request.form['searchPartCode']
    if request.form['searchPartName']:
        query["partName"] = request.form['searchPartName']
    if request.form['searchSpec']:
        query["spec"] = request.form['searchSpec']
    if request.form['searchStatus']:
        query["status"] = request.form['searchStatus']
    results = list(parts_collection.find(query))
    for part in results:
        part['_id'] = str(part['_id'])  # str 변환
    return render_template('index.html', parts=results)

@app.route('/edit/<part_id>', methods=['GET'])
def edit(part_id):
    part = parts_collection.find_one({"_id": ObjectId(part_id)})
    part['_id'] = str(part['_id'])  # 다시 넘길 수 있게 처리
    return render_template('edit.html', part=part)

@app.route('/update/<part_id>', methods=['POST'])
def update(part_id):
    updated = {
        "partCode": request.form['partCode'],
        "partName": request.form['partName'],
        "spec": request.form['spec'],
        "inDate": request.form['inDate'],
        "outDate": request.form['outDate'],
        "quantity": request.form['quantity'],
        "status": request.form['status']
    }

    if 'partImage' in request.files and request.files['partImage'].filename:
        image = request.files['partImage']
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        updated["image"] = filename

    parts_collection.update_one({"_id": ObjectId(part_id)}, {"$set": updated})
    return redirect(url_for('index'))


@app.route('/delete/<part_id>')
def delete(part_id):
    parts_collection.delete_one({"_id": ObjectId(part_id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5010)