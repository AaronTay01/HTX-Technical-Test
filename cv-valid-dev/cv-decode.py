import os
import requests
import pandas as pd
from tqdm import tqdm

# Define constants
AWS_API_URL = "http://13.213.61.168:8001/asr"
API_URL = "http://localhost:8001/asr"  # Replace with the actual API endpoint
AUDIO_FOLDER = r"cv-valid-dev"          # Folder containing audio files
CSV_FILE = "cv-valid-dev\cv-valid-dev.csv"          # CSV file with metadata
BATCH_SIZE = 50  # Number of files per batch

def transcribe_audio_files_batch(audio_files):
    """
    Sends a batch of audio files in a single POST request to the API.
    """
    files = [("files", open(file, "rb")) for file in audio_files]
    try:
        # Post Request
        response = requests.post(API_URL, files=files)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
    finally:
        for _, file in files:
            file.close()

def main():
    # Read the CSV file
    project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(project_path, CSV_FILE)  # Combine project path with the file name
    df = pd.read_csv(file_path)
    
    # Prepare the full paths of audio files
    audio_files = [os.path.join(project_path, AUDIO_FOLDER, file) for file in df["filename"]]

    # Process files in batches
    transcriptions = []
    for i in tqdm(range(0, len(audio_files), BATCH_SIZE)):
        batch = audio_files[i:i + BATCH_SIZE]
        try:
            response = transcribe_audio_files_batch(batch)
            if response:
                transcriptions.extend([result.get("transcription", "") for result in response])
            else:
                transcriptions.extend([""] * len(batch))
        except Exception as e:
            print(f"Error processing batch {i//BATCH_SIZE + 1}: {e}")
            transcriptions.extend([""] * len(batch))

    # Add the transcriptions to the DataFrame
    df["generated_text"] = transcriptions

    # Save the updated DataFrame
    df.to_csv(file_path, index=False)
    print(f"Transcriptions saved to {file_path}")

if __name__ == "__main__":
    main()
