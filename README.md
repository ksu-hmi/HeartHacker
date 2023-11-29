# Heart Hacker - Digital Stethoscope

Heart Hacker is a Python application that allows users to record audio and detect the heart rate based on the recorded audio signal. The heart rate is inferred using a fuzzy system and displayed on the graphical user interface (GUI).

## Features

- **Audio Recording:** Utilizes the PyAudio library to record audio from a low-cost microphone or the default input device.
- **Heart Rate Detection:** Analyzes the recorded audio signal to detect heart rate using a fuzzy system.
- **Graphical User Interface (GUI):** Provides a simple GUI for user interaction and displaying the recorded audio signal and detected heart rate.


- Python 3.x
- Dependencies (Install using `pip install -r requirements.txt`):
  - PyAudio
  - NumPy
  - Wavio
  - Tkinter
  - Matplotlib
  - TensorFlow
  - Pillow (PIL)

#Hardware 

- Microphone: PRO SIGNAL NPA415-OMNI Microphone or equivalent
- For Mac Laptops: USB Type C to 3.5mm Headphone Jack Adapter & TRS-TRRS Adapter

## Usage

1. Clone the repository:

   ```bash
   git clone https://github.com/ksu-hmi/HeartHacker.git
   ```

2. Navigate to the project directory:

   ```bash
   cd HeartHacker
   ```

3. Run the script:

   ```bash
   python app.py
   ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributor
Caroline Lazaro (https://github.com/lazarocf)

