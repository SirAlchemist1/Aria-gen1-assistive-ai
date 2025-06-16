#wake word test for "Hey Aria". Wake word can be changed in WAKEPHRASES
import whisper
import sounddevice as sd
import numpy as np
import tempfile
import os
import time
import scipy.io.wavfile as wavfile
from rapidfuzz import fuzz

model = whisper.load_model("base")  

WAKE_PHRASES = ["hey aria", "hey area", "hey arya"]
THRESHOLD = 80  #Fuzzy match threshold

def is_wake_phrase(text, phrases=WAKE_PHRASES, threshold=THRESHOLD):
    return any(fuzz.partial_ratio(text.lower(), phrase) >= threshold for phrase in phrases)

def record_chunk(duration=2, fs=64000):
    print("Listening...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    return audio, fs

def transcribe(audio, fs):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        wavfile.write(f.name, fs, audio)
        result = model.transcribe(f.name)
        os.remove(f.name)
        return result["text"]

print("Wake-word detection started. Say 'Hey Aria'...")

try:
    while True:
        audio_chunk, rate = record_chunk()
        text = transcribe(audio_chunk, rate)
        print("Heard:", text)

        if is_wake_phrase(text):
            print("Wake phrase detected!")
            os.system('say "Yes?"') 
            break

        time.sleep(0.01)  #change if needed

except KeyboardInterrupt:
    print("\n Exiting listener.")
