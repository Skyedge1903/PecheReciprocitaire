import json

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

polygons = []


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/save', methods=['POST'])
def save_polygon():
    data = request.json
    polygons.append(data)

    # Enregistrement dans un fichier
    with open('Lacs.json', 'w') as f:
        json.dump(polygons, f)

    return jsonify(success=True)


if __name__ == '__main__':
    app.run(debug=True)
