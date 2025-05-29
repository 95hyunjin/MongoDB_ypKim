from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index4.html")

@app.route("/chart-data")
def chart_data():
    data = {
        "labels": ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
        "values": [12, 19, 3, 5, 2, 3]
    }
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)