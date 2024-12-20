from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
from datasets import load_dataset
import torch

def transcribe_audio(example):
    # Load model and processor
    model_name = 'facebook/wav2vec2-large-960h'
    processor = Wav2Vec2Processor.from_pretrained(model_name)
    model = Wav2Vec2ForCTC.from_pretrained(model_name)
    
    # Tokenize the audio data, make sure to provide the sampling rate
    input_values = processor(example["audio"]["array"], return_tensors="pt", padding="longest", sampling_rate=16000).input_values  # Batch size 1
    
    # Retrieve logits from the model
    with torch.no_grad():  # Disable gradient calculation as we're doing inference
        logits = model(input_values).logits

    # Get the predicted ids by taking the argmax
    predicted_ids = torch.argmax(logits, dim=-1)

    # Decode the predicted ids to text
    transcription = processor.batch_decode(predicted_ids)

    # Return a dictionary with the transcription as a new column
    return {"transcription": transcription[0]}  # Return a dictionary with 'transcription' as a key

if __name__ == '__main__':
    # Load dummy dataset and read sound files
    ds = load_dataset("patrickvonplaten/librispeech_asr_dummy", "clean", split="validation", trust_remote_code=True)

    # Apply the transcription function to the dataset
    transcriptions = ds.map(transcribe_audio, remove_columns=["audio"])

    # Print a few transcriptions as examples
    for i in range(5):
        print(f"Transcription {i+1}: {transcriptions[i]['transcription']}")
 