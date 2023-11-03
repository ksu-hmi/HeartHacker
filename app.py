import pyaudio
import numpy as np
import wavio  # Import the wavio library

# Constants for audio recording
SAMPLE_RATE = 44100  # Sample rate in Hz
RECORDING_DURATION = 5  # Duration of recording in seconds

def record_audio():
    audio = pyaudio.PyAudio()

    stream = audio.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=SAMPLE_RATE,
                        input=True,
                        frames_per_buffer=1024)

    print("Recording...")
    frames = []

    for i in range(0, int(SAMPLE_RATE / 1024 * RECORDING_DURATION)):
        data = stream.read(1024)
        frames.append(data)

    print("Recording finished.")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    return np.frombuffer(b''.join(frames), dtype=np.int16)

if __name__ == "__main__":
    audio_data = record_audio()

    # Save the recorded audio to a WAV file
    wavio.write("recorded_audio.wav", audio_data, SAMPLE_RATE, sampwidth=2)

    # Process and analyze audio_data for heart rate detection
    # Implement heart rate detection algorithm and visualization here
