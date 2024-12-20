from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
import torchaudio

# Audio Speech Recognition
app = Flask(__name__)

# Load pre-trained model and processor
processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")

# Function to transcribe audio
def transcribe_audio(file_path):
    # Load audio file
    waveform, sample_rate = torchaudio.load(file_path)
    
    # Resample to 16kHz if needed
    if sample_rate != 16000:
        waveform = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)(waveform)
    
    # Preprocess the audio
    input_values = processor(waveform.squeeze().numpy(), sampling_rate=16000, return_tensors="pt").input_values
    
    # Perform inference
    logits = model(input_values).logits
    predicted_ids = logits.argmax(dim=-1)
    
    # Decode the transcription
    transcription = processor.decode(predicted_ids[0])
    
    # Get the duration of the audio in seconds
    duration = waveform.size(1) / 16000  # Assuming 16kHz sampling rate
    
    return transcription, f"{duration:.2f}"

# Function to check file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'mp3'}

@app.route('/asr', methods=['POST'])
def asr():
    if 'files' not in request.files:
        return jsonify({"error": "No files part in the request"}), 400

    files = request.files.getlist('files')

    if not files:
        return jsonify({"error": "No files selected"}), 400
    
    results = []
    tmp_dir = os.path.join(os.getcwd(), "tmp")  # Create a temporary directory in the current folder
    os.makedirs(tmp_dir, exist_ok=True)  # Ensure the directory exists
    
    for file in files:
        if file.filename == '':
            continue

        filename = secure_filename(file.filename)
        file_path = os.path.join(tmp_dir, filename)
        file.save(file_path)

        # Process the audio file to get transcription and duration
        transcription, duration = transcribe_audio(file_path)

        # Append the result to the results list
        results.append({
            "filename": filename,
            "transcription": transcription,
            "duration": duration
        })

        # Clean up the saved file
        os.remove(file_path)

    return jsonify(results)
            
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
