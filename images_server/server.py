from flask import Flask, request, jsonify
from os import makedirs, path

app = Flask(__name__)

UPLOAD_DIRECTORY = 'static/images/'

makedirs(UPLOAD_DIRECTORY, exist_ok=True)


@app.route('/upload', methods=['POST'])
def upload_image():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        filename = path.join(UPLOAD_DIRECTORY, uploaded_file.filename)
        uploaded_file.save(filename)
        return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 200
    else:
        return jsonify({'error': 'No file selected for upload'}), 400


if __name__ == '__main__':
    app.run(port=5000)
