from flask import Flask, request, jsonify, make_response
import os, base64
from flask_cors import CORS
import pandas as pd

import tempfile

app = Flask(__name__)

header = [('scorer','' , 'experimenter', 'experimenter', 'experimenter', 'experimenter', 'experimenter', 'experimenter', 'experimenter', 'experimenter', 'experimenter', 'experimenter', 'experimenter', 'experimenter', 'experimenter', 'experimenter', 'experimenter', 'experimenter', 'experimenter', 'experimenter', 'experimenter'),
            ('bodyparts', '', 'head', 'head', 'tail_1', 'tail_1', 'tail_2', 'tail_2', 'tail_3', 'tail_3', 'tail_4', 'tail_4', 'tail_5', 'tail_5', 'tail_6', 'tail_6', 'tail_7', 'tail_7', 'tail_8', 'tail_8', 'tail_9', 'tail_9'),
            ('coords', '', 'x', 'y', 'x', 'y', 'x', 'y', 'x', 'y', 'x', 'y', 'x', 'y', 'x', 'y', 'x', 'y', 'x', 'y', 'x', 'y')]

CORS(app) 
@app.route('/get_csv', methods=['POST'])
def generate_csv():
    data = []
    data.extend(header)

    coordinate_data = request.get_json()
    for video in coordinate_data:
        for image in coordinate_data[video]:
            data_entry = ['labeled-data', video]
            data_entry.append(image['path'])
            coordinates = image['coordinates']

            i = 0
            while i < min(10, len(coordinates)):
                data_entry.append(coordinates[i]["x"])
                data_entry.append(coordinates[i]["y"])
                i += 2
            
            while i < 10:
                data_entry.append('')
                i += 1
            
            data.append(data_entry)
    print(coordinate_data)


    df = pd.DataFrame(data)
    resp = make_response(df.to_csv(index=False, header=False))
    resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
    resp.headers["Content-Type"] = "text/csv"
    return resp


# @app.route('/get_images', methods=['GET'])


if __name__ == '__main__':
    app.run(debug=True)