from pymongo import MongoClient
from pprint import pprint

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# MongoDB 연결
client = MongoClient("mongodb://localhost:27017/")
db = client["TUE_db"]
collection = db["examples"]

exampels = {
  "drawing_name": "Hull Plan",
  "category": "Structure",
  "versions": [
    {
      "version_no": 1,
      "updated_by": "Kim",
      "update_date": "2024-01-01"
    },
    {
      "version_no": 2,
      "updated_by": "Lee",
      "update_date": "2024-02-15"
    }
  ]
}
