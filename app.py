#Importing the necessary libraries pyaudio for audiorecording, numpy for data manipulation, and wavio for saving the recorded audio 
import pyaudio
import numpy as np
import wavio  # Import the wavio library

# Constants for audio recording
SAMPLE_RATE = 44100  # Sample rate in Hz
RECORDING_DURATION = 5  # Duration of recording in seconds

#Creating the record_audio function- it initializes a PyAudio object, opens an audio stream with the specified parameters, records audio data for a specified duration and saves it in a list called 'frames'
def record_audio():
    audio = pyaudio.PyAudio()

    stream = audio.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=SAMPLE_RATE,
                        input=True,
                        frames_per_buffer=1024)

#Recording process: The code prints "Reocording" to indicate that audio recording has started. It records the audio in chunks for the specified duration and appends each chunk to the frames list
    print("Recording...")
    frames = []

    for i in range(0, int(SAMPLE_RATE / 1024 * RECORDING_DURATION)):
        data = stream.read(1024)
        frames.append(data)

    print("Recording finished.")

#After recording is finished, the script stops the audio stream, closes it, and terminates the PyAudio object
    stream.stop_stream()
    stream.close()
    audio.terminate()

    return np.frombuffer(b''.join(frames), dtype=np.int16)

#The code then saves the recorded audio to a WAV file named "recorded_audio.wav" in the same directory as the script using the wavio.write function
if __name__ == "__main__":
    audio_data = record_audio()

# Save the recorded audio to a WAV file
    wavio.write("recorded_audio.wav", audio_data, SAMPLE_RATE, sampwidth=2)

# Process and analyze audio_data for heart rate detection
# Implement heart rate detection algorithm and visualization here
