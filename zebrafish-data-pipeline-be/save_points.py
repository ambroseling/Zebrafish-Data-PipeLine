from flask import Flask, request, jsonify
import os, base64
from flask_cors import CORS
import psycopg2 as pg

import tempfile

app = Flask(__name__)

def get_db_connection():
    try:
        conn = pg.connect(host='localhost',
                                database='zebrafish_test',
                                options="-c search_path=zebrafishschema"
                                )
        return conn
    except pg.Error:  
        return False  

CORS(app) 
@app.route('/', methods=['POST'])
def extract_images():
    fish_video = request.form['fish_video']
    img = request.form['image']

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO Video (fish_video, img) VALUES (%s, %s)',
            (fish_video, img))
    conn.commit()
    cur.close()
    conn.close()
    return 'Success!'

# @app.route('/get_images', methods=['GET'])


if __name__ == '__main__':
    app.run(debug=True)