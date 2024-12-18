from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
# from datasets import load_dataset
# import torch


# Audio Speech Recognition
app = Flask(__name__)

# Function to check file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'mp3'}

@app.route('/asr', methods=['POST'])
def asr():
    if 'file' in request.files:
        return jsonify({'error', 'No File Found'}, 400)
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        # Check if the file exists in the request (it exists in memory)
        return jsonify({'message': f"File '{file.filename}' exists in memory"}), 200

    return jsonify({'error': 'Invalid file format'}), 400


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8001)
