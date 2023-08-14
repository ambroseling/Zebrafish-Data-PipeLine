from flask import Flask, request, jsonify,make_response

import os, base64
from flask_cors import CORS  # Import the CORS extension

import pandas as pd

import tempfile

import cv2
import tempfile
import json

app = Flask(__name__)

CORS(app) 
@app.route('/save_json', methods=['POST'])
def save_json():
    try:
        data = request.get_json()  # Get JSON data from the request
        # Save the JSON data to a file
        with open('data.json', 'w') as file:
            file.write(json.dumps(data, indent=4))
        return jsonify({'message': 'JSON data saved successfully.'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/extract_images', methods=['POST'])
def extract_images():
    # Get the uploaded videos from the request
    #data = request.get_json()
    #print("RECEIVED DATA: ",data)
    data_path =  "/Users/ambroseling/Desktop/zebrafish-data-pipeline/data"
    uploaded_files = request.files.getlist('videos')
    # Sample rate (number of frames to skip between each extracted frame)
    print("SAMPLE RATE:")
    sample_rate = int(request.form.get('sample_rate', 10))
    print(sample_rate)
    # Temporary directory to store extracted images
    with tempfile.TemporaryDirectory() as tmpdirname:
        
        extracted_images = []
        # Process each uploaded video
        for video in uploaded_files:
            video_path = os.path.join(tmpdirname, video.filename)
            video.save(video_path)

            # Read video using OpenCV
            cap = cv2.VideoCapture(video_path)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            print("FRAME COUNT")
            print(frame_count)
            extracted_images_per_vid = []
            # Extract frames at the specified sample rate
            for frame_number in range(0, frame_count, sample_rate):
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
                ret, frame = cap.read()
                if ret:
                    image_path = os.path.join(data_path, f"{video.filename}_frame_{frame_number}.jpg")
                    cv2.imwrite(image_path, frame)
                    extracted_images_per_vid.append(image_path)
            extracted_images.append(extracted_images_per_vid)
            cap.release()
        print(len(extracted_images))
        # Return the paths of extracted images
        return jsonify(extracted_images)

@app.route('/get_images', methods=['GET'])
def get_images():
    image_directory = '/Users/ambroseling/Desktop/zebrafish-data-pipeline/data'
    image_data_list = []

    # Iterate through the image files in the directory
    for filename in os.listdir(image_directory):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            image_path = os.path.join(image_directory, filename)

            # Read the image file from the file system
            with open(image_path, 'rb') as image_file:
                image_data = image_file.read()

            # Convert the image data to base64 encoding
            base64_image = base64.b64encode(image_data).decode('utf-8')

            # Append the base64-encoded image data to the list
            image_data_list.append({'filename': filename, 'data': base64_image})
            os.remove(image_path)

    # Return the list of base64-encoded image data in the JSON response
    return jsonify({'images': image_data_list})

header = [('scorer','' , '', 'experimenter', 'experimenter', 'experimenter', 'experimenter', 'experimenter', 'experimenter', 'experimenter', 'experimenter', 'experimenter', 'experimenter', 'experimenter', 'experimenter', 'experimenter', 'experimenter', 'experimenter', 'experimenter', 'experimenter', 'experimenter', 'experimenter'),
            ('bodyparts', '', '', 'head', 'head', 'tail_1', 'tail_1', 'tail_2', 'tail_2', 'tail_3', 'tail_3', 'tail_4', 'tail_4', 'tail_5', 'tail_5', 'tail_6', 'tail_6', 'tail_7', 'tail_7', 'tail_8', 'tail_8', 'tail_9', 'tail_9'),
            ('coords', '', '', 'x', 'y', 'x', 'y', 'x', 'y', 'x', 'y', 'x', 'y', 'x', 'y', 'x', 'y', 'x', 'y', 'x', 'y', 'x', 'y')]

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
                i += 1
            while i < 10:
                data_entry.append('')
                i += 1
            
            data.append(data_entry)


    df = pd.DataFrame(data)
    resp = make_response(df.to_csv(index=False, header=False))
    resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
    resp.headers["Content-Type"] = "text/csv"
    return resp


# @app.route('/get_images', methods=['GET'])


if __name__ == '__main__':
    app.run(debug=True)


if __name__ == '__main__':
    app.run(debug=True)