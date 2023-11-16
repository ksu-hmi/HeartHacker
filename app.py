#Importing the necessary libraries pyaudio for audiorecording, numpy for data manipulation, and wavio for saving the recorded audio 
import pyaudio
import numpy as np
import wavio  
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
 
# Constants for audio recording including sample rate and the recording duration

SAMPLE_RATE = 44100  # Sample rate in Hz
RECORDING_DURATION = 20  # Duration of recording in seconds

# Global variable to check if recording is in progress
is_recording = False


#Creating the record_audio function- it initializes a PyAudio object, opens an audio stream with the specified parameters, records audio data for a specified duration and saves it in a list called 'frames'
def record_audio(input_device_index=None, input_gain=1.0):
    global is_recording
    audio = pyaudio.PyAudio()

    stream = audio.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=SAMPLE_RATE,
                        input=True,
                        input_device_index=input_device_index,
                        frames_per_buffer=1024)
    
    #Recording process: The code prints "Recording" to indicate that audio recording has started. It records the audio in chunks for the specified duration and appends each chunk to the frames list

#Recording process: The code prints "Recording" to indicate that audio recording has started. It records the audio in chunks for the specified duration and appends each chunk to the frames list
    print("Recording...")
    frames = []

    for i in range(0, int(SAMPLE_RATE / 1024 * RECORDING_DURATION)):
        if not is_recording:
            break
        data = stream.read(1024)
        frames.append(data)

    print("Recording finished.")

    #After recording is finished, the script stops the audio stream, closes it, and terminates the PyAudio object

#After recording is finished, the script stops the audio stream, closes it, and terminates the PyAudio object
    stream.stop_stream()
    stream.close()
    audio.terminate()

    return np.frombuffer(b''.join(frames), dtype=np.int16)


######################################

#HeartRate Detection Function 

import matplotlib.pyplot as plt
from scipy.signal import find_peaks

def detect_heart_rate(audio_data, sample_rate):
    # Plot the time-domain signal (audio waveform)
    time = np.arange(0, len(audio_data)) / sample_rate
    fig, ax = plt.subplots()
    plt.plot(time, audio_data)
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude')
    plt.title('Time-Domain Signal (Audio Waveform)')
    plt.show()
    plot_canvas.draw()


    # Find peaks in the audio waveform
    peaks, _ = find_peaks(audio_data, height=0)

    # Calculate heart rate based on the detected peaks
    heart_rate = 60 / np.diff(time[peaks]).mean()  # Calculate heart rate from time intervals between peaks
    
    # Display heart rate on the GUI
    result_label.config(text=f"Detected Heart Rate: {heart_rate:.2f} beats per minute")


# Function to start recording
def start_recording():
    global is_recording
    is_recording = True
    audio_data = record_audio()
    is_recording = False
    detect_heart_rate(audio_data, SAMPLE_RATE, plot_canvas)

# GUI setup
root = tk.Tk()
root.title("Heart Rate Recorder")

# Create a button to start recording
start_button = tk.Button(root, text="Start Recording", command=start_recording)
start_button.pack(pady=10)

# Create a label to display the result
result_label = tk.Label(root, text="")
result_label.pack(pady=10)

# Create a canvas for embedding the matplotlib plot
plot_canvas = FigureCanvasTkAgg(plt.figure(), master=root)
plot_canvas.get_tk_widget().pack()

# Start the GUI event loop
root.mainloop()