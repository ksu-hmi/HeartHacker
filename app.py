#Importing the necessary libraries pyaudio for audiorecording, numpy for data manipulation, and wavio for saving the recorded audio 
import pyaudio
import numpy as np
import wavio  
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from dataclasses import dataclass
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tempfile
import tensorflow as tf
from urllib.request import urlopen
from PIL import Image, ImageTk
from io import BytesIO
import ssl
import matplotlib.pyplot as plt

ssl._create_default_https_context = ssl._create_default_https_context

# Set the path to the CA bundle
cafile = "/etc/ssl/cert.pem"
ssl_context = ssl.create_default_context(cafile=cafile)

# Constants for audio recording including sample rate and the recording duration
SAMPLE_RATE = 44100  # Sample rate in Hz
RECORDING_DURATION = 10  # Duration of recording in seconds

# Global variable to check if recording is in progress
is_recording = False
global_plot_canvas = None


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

@dataclass
class FuzzySet:
    """
    A class for representing and manipulating triangular fuzzy sets.
    """

    name: str
    left_boundary: float
    peak: float
    right_boundary: float

    def __str__(self) -> str:
        return f"{self.name}: [{self.left_boundary}, {self.peak}, {self.right_boundary}]"

    def complement(self) -> 'FuzzySet':
        return FuzzySet(
            f"¬{self.name}",
            1 - self.right_boundary,
            1 - self.left_boundary,
            1 - self.peak,
        )

    def intersection(self, other) -> 'FuzzySet':
        return FuzzySet(
            f"{self.name} ∩ {other.name}",
            max(self.left_boundary, other.left_boundary),
            min(self.right_boundary, other.right_boundary),
            (self.peak + other.peak) / 2,
        )

    def membership(self, x: float) -> float:
        if x <= self.left_boundary or x >= self.right_boundary:
            return 0.0
        elif self.left_boundary < x <= self.peak:
            return (x - self.left_boundary) / (self.peak - self.left_boundary)
        elif self.peak < x < self.right_boundary:
            return (self.right_boundary - x) / (self.right_boundary - self.peak)
        msg = f"Invalid value {x} for fuzzy set {self}"
        raise ValueError(msg)

    def union(self, other) -> 'FuzzySet':
        return FuzzySet(
            f"{self.name} ∪ {other.name}",
            min(self.left_boundary, other.left_boundary),
            max(self.right_boundary, other.right_boundary),
            (self.peak + other.peak) / 2,
        )

    def plot(self):
        x = np.linspace(0, 1, 1000)
        y = [self.membership(xi) for xi in x]

        plt.plot(x, y, label=self.name)


class HeartRateFuzzySystem:
    def __init__(self):
        self.high_peak = FuzzySet("HighPeak", 0.7, 1, 1)
        self.low_amplitude = FuzzySet("LowAmplitude", 0, 0.3, 0.5)
        self.low_rate = FuzzySet("LowRate", 0, 0, 0.3)
        self.medium_rate = FuzzySet("MediumRate", 0.2, 0.5, 0.8)
        self.high_rate = FuzzySet("HighRate", 0.7, 1, 1)

    def infer_heart_rate(self, peak, amplitude):
        high_peak_membership = self.high_peak.membership(peak)
        low_amplitude_membership = self.low_amplitude.membership(amplitude)

        low_rate = min(high_peak_membership, low_amplitude_membership)
        medium_rate = min(high_peak_membership, 1 - low_amplitude_membership)
        high_rate = 1 - low_rate - medium_rate

        result = (
            low_rate * self.low_rate.peak
            + medium_rate * self.medium_rate.peak
            + high_rate * self.high_rate.peak
        ) / (low_rate + medium_rate + high_rate)

        return result


# Global variable for fuzzy system
fuzzy_system = HeartRateFuzzySystem()

#HeartRate Detection Function 

import matplotlib.pyplot as plt
from scipy.signal import find_peaks

def detect_heart_rate(audio_data, sample_rate):
    global global_plot_canvas, fuzzy_system
    time = np.arange(0, len(audio_data)) / sample_rate
    fig, ax = plt.subplots()
    ax.plot(time, audio_data)
    ax.set_xlabel('Time (seconds)')
    ax.set_ylabel('Amplitude')
    ax.set_title('Audio Signal') 

# Check if global_plot_canvas is set
    if global_plot_canvas:
        global_plot_canvas.get_tk_widget().destroy()  # Destroy previous canvas
    global_plot_canvas = FigureCanvasTkAgg(fig, master=root)
    global_plot_canvas.draw()
    global_plot_canvas.get_tk_widget().pack()

  # Only consider peaks above or below 5000 amps as heartbeats to cancel out the other noise 
    peaks, _ = find_peaks(np.abs(audio_data), height=5000)

    # Calculate heart rate based on the detected peaks
    heart_rate = 60 / (2 * np.diff(time[peaks]).mean())
    
    # Display heart rate on the GUI
    result_label.config(text=f"Detected Heart Rate: {heart_rate:.2f} beats per minute")

   # Save the recorded audio as a temporary WAVE file
    temp_wav_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    wavio.write(temp_wav_file.name, audio_data, sample_rate, sampwidth=3)
 # Run the TensorFlow script for audio classification
    labels_file = "path/to/your/labels.txt"  # Update with the correct path
    graph_file = "path/to/your/model.pb"  # Update with the correct path

    tf.compat.v1.flags.DEFINE_string("wav", temp_wav_file.name, "Path to the recorded audio file.")
    tf.compat.v1.flags.DEFINE_string("labels", labels_file, "Path to the file containing labels.")
    tf.compat.v1.flags.DEFINE_string("graph", graph_file, "Path to the frozen graph file.")
    tf.compat.v1.flags.DEFINE_string("input_name", "wav_data:0", "Name of WAVE data input node in model.")
    tf.compat.v1.flags.DEFINE_string("output_name", "labels_softmax:0", "Name of node outputting a prediction in the model.")
    tf.compat.v1.flags.DEFINE_integer("how_many_labels", 3, "Number of results to show.")

    FLAGS = tf.compat.v1.flags.FLAGS

    label_wav(FLAGS.wav, FLAGS.labels, FLAGS.graph, FLAGS.input_name, FLAGS.output_name, FLAGS.how_many_labels)


    temp_wav_file.close()
def label_wav(wav, labels, graph, input_name, output_name, how_many_labels):
    # Add your code for audio classification here
    # This function should load the TensorFlow model and classify the audio
    pass
# Function to start recording
def start_recording():
    global is_recording
    global global_plot_canvas
    is_recording = True
    audio_data = record_audio()
    is_recording = False
    detect_heart_rate(audio_data, SAMPLE_RATE)

    # Function to restart the process
def restart_process():
    global global_plot_canvas, result_label
    # Destroy the previous plot canvas
    if global_plot_canvas:
        global_plot_canvas.get_tk_widget().destroy()
        global_plot_canvas = None
    # Clear the result label
    result_label.config(text="")
    # Restart recording
    start_recording()

# GUI setup
root = tk.Tk()
root.title("Heart Rate Recorder")

# Loading the logo image from GitHub
logo_url = 'https://raw.githubusercontent.com/ksu-hmi/HeartHacker/main/HeartHacker.png'
logo_image_bytes = urlopen(logo_url, context=ssl_context).read()
logo_image = Image.open(BytesIO(logo_image_bytes))
# Setting desired width and height for resizing
width, height = 400, 200
logo_image = logo_image.resize((width, height))
logo_image = ImageTk.PhotoImage(logo_image)

# Loading the images for recording and restart buttons from GitHub
recording_button_url = 'https://github.com/ksu-hmi/HeartHacker/raw/main/start.png'
recording_button_image_bytes = urlopen(recording_button_url, context=ssl_context).read()
recording_button_image = Image.open(BytesIO(recording_button_image_bytes))
recording_button_image = ImageTk.PhotoImage(recording_button_image)

restart_button_url = 'https://github.com/ksu-hmi/HeartHacker/raw/main/restart.png'
restart_button_image_bytes = urlopen(restart_button_url, context=ssl_context).read()
restart_button_image = Image.open(BytesIO(restart_button_image_bytes))
restart_button_image = ImageTk.PhotoImage(restart_button_image)

# Create a label for the logo image
logo_label = tk.Label(root, image=logo_image)
logo_label.pack(pady=10)

# Resize the images for buttons
width, height = 50, 50  # Adjust the width and height as needed
recording_button_image = Image.open(BytesIO(recording_button_image_bytes)).resize((width, height))
recording_button_image = ImageTk.PhotoImage(recording_button_image)

restart_button_image = Image.open(BytesIO(restart_button_image_bytes)).resize((width, height))
restart_button_image = ImageTk.PhotoImage(restart_button_image)

# Create a button to start recording
start_button = tk.Button(root, image=ImageTk.PhotoImage(recording_button_image), command=start_recording)
start_button.pack(side=tk.LEFT, padx=5)

# Create a button to restart the process
restart_button = tk.Button(root, image=ImageTk.PhotoImage(restart_button_image), command=restart_process)
restart_button.pack(side=tk.LEFT, padx=5)

# Create a label to display the result
result_label = tk.Label(root, text="")
result_label.pack(pady=10)

# Create a canvas for embedding the matplotlib plot
plot_canvas = tk.Canvas(root)
plot_canvas.pack()

# Start the GUI event loop
root.mainloop()