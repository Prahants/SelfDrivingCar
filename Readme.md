# Self-Driving Car using Arduino and Python

This project implements a self-driving car system using an Arduino-controlled robot car and a Python-based neural network for image classification and control. The system uses an Android smartphone as an IP camera to capture the road/environment and sends commands to the Arduino via Bluetooth or Serial connection.

## Project Overview

The project consists of three main components:
1.  **Data Collection (`sdc.py`)**: A GUI application to manually control the car and collect training data (images labeled with directions: forward, left, right).
2.  **Model Training (`trainsdc.py`)**: A script to train a Neural Network (MLPClassifier) on the collected image data.
3.  **Autonomous Driving (`drivercar.py`)**: A script that uses the trained model to predict steering directions from live camera feed and drive the car autonomously.

## Prerequisites

### Hardware
*   Arduino-based Robot Car (with Bluetooth/Serial module).
*   Android Smartphone with **IP Webcam** app installed.
*   PC/Laptop with Python installed.

### Software & Libraries
*   Python 3.x
*   **Android App**: [IP Webcam](https://play.google.com/store/apps/details?id=com.pas.webcam&hl=en)

### Python Dependencies
The following libraries are required to run the project. Install them using `pip`:

```bash
pip install pyserial PyQt5 scikit-image scikit-learn numpy opencv-python matplotlib joblib
```

**Library Details:**
*   **PyQt5**: Used for the GUI application (`sdc.py`) to control the car and collect data.
*   **pyserial**: Used for serial communication between Python and Arduino.
*   **scikit-image**: Used for image processing (loading, saving, resizing).
*   **scikit-learn**: Used for the Neural Network implementation (MLPClassifier).
*   **numpy**: Used for numerical operations and array handling.
*   **opencv-python** (`cv2`): Used for computer vision tasks (image resizing, thresholding, blurring).
*   **matplotlib**: Used for image loading in helper scripts.
*   **joblib**: Used for saving and loading the trained model.

## Setup & Configuration

**Important**: The code contains hardcoded paths and configurations that you **must** update for your environment.

1.  **Camera URL**:
    *   Open `sdc.py` and `drivercar.py`.
    *   Update the `url` variable with your IP Webcam address (e.g., `http://192.168.1.x:8080/shot.jpg`).

2.  **Serial Port**:
    *   Check which COM port your Arduino is connected to (e.g., `COM3`, `/dev/ttyUSB0`).
    *   Update the `COM` port in `sdc.py` (GUI input) and `drivercar.py` (`serial.Serial('COM10', 9600)`).

3.  **Data Directories**:
    *   Create a folder named `testsdc` in your project directory (or wherever you want to save images).
    *   Open `sdc.py` and update the image save paths (currently `C:\python35\testsdc\...`) to your local `testsdc` folder path.
    *   Update `trainsdc.py` to point to this `testsdc` folder for loading training data.

## Usage Guide

### Step 1: Data Collection
1.  Run the data collection GUI:
    ```bash
    python sdc.py
    ```
2.  Enter your COM port (e.g., `COM3`) and Camera URL.
3.  Click **Start** to open the connection.
4.  Use the on-screen buttons (**Forward**, **Left**, **Right**, **Backward**, **Stop**) to drive the car.
5.  Each click sends a command to the car and saves a snapshot from the camera labeled with the direction.
    *   *Note*: Ensure the `testsdc` folder exists and paths are correct in the script.

### Step 2: Training the Model
1.  After collecting enough data, run the training script:
    ```bash
    python trainsdc.py
    ```
2.  This script reads images from the `testsdc` folder, preprocesses them, and trains a Neural Network.
3.  **Note**: The current `trainsdc.py` prints the accuracy score but **does not save** the trained model to a file automatically. You will need to add code to save the model (e.g., using `joblib.dump(alg, 'mymodel.mkl')`) so it can be used by the driving script.

### Step 3: Autonomous Driving
1.  Ensure you have a trained model file named `mymodel.mkl` (and optionally `scalermodel.pkl` if you use scaling).
2.  Run the autonomous driving script:
    ```bash
    python drivercar.py
    ```
3.   The car will start fetching images from the camera, predicting the direction, and sending commands to the Arduino to drive autonomously.

## File Structure
*   `sdc.py`: PyQt5 GUI for manual control and data collection.
*   `trainsdc.py`: Script to train the Neural Network.
*   `drivercar.py`: Main script for autonomous driving using the trained model.
*   `utils2.py`: Utility functions for image preprocessing and augmentation (used in advanced training, if applicable).

## Troubleshooting
*   **Connection Error**: Check your COM port and ensure the Arduino is connected.
*   **Camera Error**: Ensure the Android device and PC are on the same Wi-Fi network and the IP address is correct.
*   **Path Errors**: Python uses backslashes `\` for Windows paths. Ensure you use raw strings `r'path'` or double backslashes `\\` to avoid errors, or forward slashes `/` on Linux/Mac.
