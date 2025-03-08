from flask import Flask, jsonify
import json

app = Flask(__name__)

def read_data():
    with open('data.json') as f:
        data = json.load(f)
    return data

@app.route('/api', methods=['GET'])
def get_data():
    try:
        data = read_data()
        return jsonify({"status": "success", "data": data}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    

if __name__ == '__main__':
    app.run(debug=True)