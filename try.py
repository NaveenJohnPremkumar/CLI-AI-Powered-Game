import torch
import pygame
import numpy as np
import pyaudio
import whisper
import wave
import io

def speech_to_text(audio_data, model, rate):
    """ Convert raw audio waveform to text using Whisper """
    np_audio = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0  # Normalize to [-1, 1]
    
    # Convert the NumPy array into a temporary WAV file in memory
    wav_buffer = io.BytesIO()
    with wave.open(wav_buffer, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit audio
        wf.setframerate(rate)
        wf.writeframes(audio_data)
    
    wav_buffer.seek(0)  # Reset buffer position
    
    # Transcribe using Whisper
    transcript = model.transcribe(wav_buffer)
    return transcript["text"]

def record_audio(stream, frames, chunk=1024):
    """ Capture audio and append it to frames list """
    data = stream.read(chunk, exception_on_overflow=False)
    frames.append(data)

def main():
    pygame.init()
    model = whisper.load_model("whisper/base.en.pt")  # Load the correct model
    push_to_talk_key = pygame.K_SPACE
    recording = False
    rate = 44100  # Sample rate
    chunk = 1024  # Buffer size

    # Initialize PyAudio
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=rate, input=True, frames_per_buffer=chunk)
    frames = []

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == push_to_talk_key:
                if not recording:
                    recording = True
                    frames = []
                    print("Recording started...")

            if event.type == pygame.KEYUP and event.key == push_to_talk_key:
                if recording:
                    recording = False
                    print("Recording stopped...")

                    # Capture the raw waveform
                    audio_data = b''.join(frames)
                    transcription = speech_to_text(audio_data, model, rate)
                    print("Transcription:", transcription)

            if event.type == pygame.QUIT:
                stream.stop_stream()
                stream.close()
                audio.terminate()
                pygame.quit()
                return

        # If recording, continuously collect audio
        if recording:
            record_audio(stream, frames, chunk)

if __name__ == "__main__":
    main()
