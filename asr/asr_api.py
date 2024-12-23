import logging
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import io
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
import torchaudio
torchaudio.set_audio_backend("sox_io")

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Audio Speech Recognition
app = Flask(__name__)

# Load pre-trained model and processor
try:
    logger.info("Loading pre-trained models and processor...")
    processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
    model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")
    logger.info("Models loaded successfully.")
except Exception as e:
    logger.error(f"Error loading models: {e}")
    raise

# Function to transcribe audio
def transcribe_audio(file_data):
    try:
        # Load audio file from bytes
        logger.info("Processing audio file in memory...")
        waveform, sample_rate = torchaudio.load(file_data)

        # Resample to 16kHz if needed
        if sample_rate != 16000:
            logger.info(f"Resampling from {sample_rate} Hz to 16000 Hz")
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
        logger.info(f"Transcription: {transcription}, Duration: {duration:.2f} seconds")
        
        return transcription, f"{duration:.2f}"
    except Exception as e:
        logger.error(f"Error processing audio file: {e}")
        return None, None

# Function to check file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'mp3'}

@app.route('/asr', methods=['POST'])
def asr():
    try:
        if 'files' not in request.files:
            logger.error("No files part in the request")
            return jsonify({"error": "No files part in the request"}), 400

        files = request.files.getlist('files')

        if not files:
            logger.error("No files selected")
            return jsonify({"error": "No files selected"}), 400
        
        results = []
        
        for file in files:
            if file.filename == '':
                continue

            # Process the audio file directly from memory
            filename = secure_filename(file.filename)
            file_data = io.BytesIO(file.read())  # Read file into memory

            # Process the audio file to get transcription and duration
            transcription, duration = transcribe_audio(file_data)

            if transcription is None:
                continue  # Skip the file if an error occurred

            # Append the result to the results list
            results.append({
                "filename": filename,
                "transcription": transcription,
                "duration": duration
            })

        if not results:
            logger.error("No valid transcriptions found.")
            return jsonify({"error": "No valid transcriptions found."}), 500
        
        return jsonify(results)
    
    except Exception as e:
        logger.error(f"Error during ASR process: {e}")
        return jsonify({"error": f"Internal server error: {e}"}), 500
            

if __name__ == '__main__':
    logger.info("Starting Flask app...")
    app.run(host='0.0.0.0', port=8001)
