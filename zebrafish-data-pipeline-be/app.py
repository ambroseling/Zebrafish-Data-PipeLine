from flask import Flask, request, jsonify, send_file
import os, base64, zipfile
from flask_cors import CORS  # Import the CORS extension
from io import BytesIO



import cv2
import tempfile

app = Flask(__name__)

CORS(app) 
@app.route('/extract_images', methods=['POST'])
def extract_images():
    # Get the uploaded videos from the request
    #data = request.get_json()
    #print("RECEIVED DATA: ",data)
    data_path =  "../data"
    uploaded_files = request.files.getlist('videos')
    print("UPLOADED FILES:")
    print(uploaded_files)
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
    image_directory = '../data'
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
            # os.remove(image_path)

    # Return the list of base64-encoded image data in the JSON response
    return jsonify({'images': image_data_list})


@app.route('/download_images', methods=['GET'])
def download_images():
    image_directory = '../data'

    memory_file = BytesIO()
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for filename in os.listdir(image_directory):
            if filename.endswith('.jpg') or filename.endswith('.png'):
                image_path = os.path.join(image_directory, filename)
                zipf.write(image_path, os.path.relpath(image_path, image_directory))
                os.remove(image_path)

    memory_file.seek(0)
    return send_file(
        memory_file,
        mimetype='application/zip',
        as_attachment=True,
        download_name='extracted_frames.zip'
    )


if __name__ == '__main__':
    app.run(debug=True)