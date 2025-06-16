#Speech to text using whisper and using laptop microphone
import whisper
import sounddevice as sd
import numpy as np
import tempfile
import os
import scipy.io.wavfile as wavfile

model = whisper.load_model("base")  # or "tiny", "small", etc.

def record_audio(duration=5, fs=16000):
    print("Recording...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    print("Recording complete.")
    return recording, fs

def transcribe(recording, fs):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        wavfile.write(f.name, fs, recording)
        print("Transcribing...")
        result = model.transcribe(f.name)
        os.remove(f.name)
        return result["text"]

# Example usage:
audio, rate = record_audio(duration=4)
text = transcribe(audio, rate)
print("You said:", text)
