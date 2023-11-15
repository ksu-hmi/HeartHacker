#Importing the necessary libraries pyaudio for audiorecording, numpy for data manipulation, and wavio for saving the recorded audio 
import pyaudio
import numpy as np
import wavio  
 
# Constants for audio recording including sample rate and the recording duration

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

#Recording process: The code prints "Reocording" to indicate that audio recording has started. It records the audio in chunks for the specified duration and appends each chunk to the frames list
    print("Recording...")
    frames = []

    for i in range(0, int(SAMPLE_RATE / 1024 * RECORDING_DURATION)):
        data = stream.read(1024)
        frames.append(data)

    print("Recording finished.")

    #After recording is finished, the script stops the audio stream, closes it, and terminates the PyAudio object

#After recording is finished, the script stops the audio stream, closes it, and terminates the PyAudio object
    stream.stop_stream()
    stream.close()
    audio.terminate()

    return np.frombuffer(b''.join(frames), dtype=np.int16)

if __name__ == "__main__":
    audio_data = record_audio()

# Save the recorded audio to a WAV file
    wavio.write("recorded_audio.wav", audio_data, SAMPLE_RATE, sampwidth=2)


######################################

#HeartRate Detection Function 

import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# Function to detect heart rate from audio
def detect_heart_rate(audio_data, sample_rate):
    # Perform Fast Fourier Transform (FFT) to get frequency domain representation
    fft_result = np.fft.fft(audio_data)
    frequencies = np.fft.fftfreq(len(fft_result), d=1/sample_rate)
    
    # Keep only positive frequencies
    positive_frequencies = frequencies[frequencies > 0]
    positive_fft = fft_result[frequencies > 0]
    
    # Plot the frequency spectrum
    plt.plot(positive_frequencies, np.abs(positive_fft))
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.title('Frequency Spectrum')
    plt.show()

    # Find peaks in the frequency spectrum
    peaks, _ = find_peaks(np.abs(positive_fft), height=500)

    # Calculate heart rate based on the detected peaks
    heart_rate = positive_frequencies[peaks[0]]
    
    return heart_rate

if __name__ == "__main__":
    audio_data = record_audio()
    heart_rate = detect_heart_rate(audio_data, SAMPLE_RATE)
    
    print(f"Detected Heart Rate: {heart_rate} beats per minute")

