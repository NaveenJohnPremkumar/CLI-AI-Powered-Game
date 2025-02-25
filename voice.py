import time
import pyaudio
import numpy as np
import whisper
import keyboard  # For detecting spacebar press

# Audio recording settings
INPUT_FORMAT = pyaudio.paInt16
INPUT_CHANNELS = 1
INPUT_RATE = 16000
INPUT_CHUNK = 1024

# Load Whisper model once
model = whisper.load_model("base.en")

def speech_to_text(waveform):
    transcript = model.transcribe(waveform, fp16=False)
    return transcript["text"]

def waveform_from_mic() -> np.ndarray:
    audio = pyaudio.PyAudio()
    stream = audio.open(format=INPUT_FORMAT, 
                        channels=INPUT_CHANNELS,
                        rate=INPUT_RATE, 
                        input=True,
                        frames_per_buffer=INPUT_CHUNK)

    frames = []

    print("Hold SPACEBAR to record...")
    while not keyboard.is_pressed("space"):
        pass  # Wait for spacebar to be pressed

    print("Recording... Release SPACEBAR to stop.")
    while keyboard.is_pressed("space"):
        data = stream.read(INPUT_CHUNK)
        frames.append(data)

    print("Recording stopped.")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Convert to numpy array
    waveform = np.frombuffer(b''.join(frames), dtype=np.int16).astype(np.float32) / 32768.0
    return waveform

def main():
    waveform = waveform_from_mic()
    if len(waveform) == 0:
        print("No audio recorded.")
        return

    text = speech_to_text(waveform)
    print("Transcription:", text)

if __name__ == "__main__":
    main()
