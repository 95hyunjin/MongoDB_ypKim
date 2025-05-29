from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import pandas as pd
from bson import ObjectId
import os
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# MongoDB 연결
client = MongoClient("mongodb://localhost:27017/")
db = client["example_db"]
collection = db["lists"]

def insert_excel_data():
    df = pd.read_excel("부품_기본정보.xlsx")
    collection.delete_many({})
    collection.insert_many(df.to_dict(orient="records"))

@app.route('/', methods=['GET', 'POST'])
def index():
	lists = list(collection.find())
	return render_template('index3.html', lists=lists)

@app.route('/add', methods=['POST'])
def add():
	product_id = request.form['product_id']
	product_name = request.form['product_name']
	cata = request.form['cata']
	company = request.form['company']
	quantity = request.form['quantity']
	etc = request.form['etc']
		

	data = {
		"부품ID": product_id,
		"부품명": product_name,
		"카테고리": cata,
		"제조사": company,
		"재고": quantity,
		"설명": etc,
	}

	image = request.files['image']
	if image and image.filename != '':
		filename = secure_filename(image.filename)
		image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
		image.save(image_path)
		data["이미지"] = filename
	else:
		data["이미지"] = ""

	collection.insert_one(data)
	return redirect(url_for('index'))


if __name__ == '__main__':
    insert_excel_data()  $excel데이터 밀어넣고
    app.run(debug=True, host='0.0.0.0', port=5002)