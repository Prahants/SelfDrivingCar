from skimage import io
from sklearn.externals import joblib
import os
import sys
import time
import serial
global url
import numpy
import cv2
# Set the camera URL (Ensure this matches your IP Webcam address)
url="http://192.168.43.1:8080/shot.jpg"

# Initialize Serial connection to Arduino (Update 'COM10' to your correct port)
s=serial.Serial('COM10',9600)
# Wait for connection to stabilize
time.sleep(2)

# Load the trained machine learning model
alg=joblib.load('mymodel.mkl')
# Optional: Load scaler if you used one during training
#scaler=joblib.load('scalermodel.pkl')
print('model loaded')

def drive():
    """
    Main loop for autonomous driving:
    1. Fetch image from camera.
    2. Preprocess image (blur, threshold, resize).
    3. Predict direction using loaded model.
    4. Send control command to Arduino.
    """
    # 1. Fetch image
    img=io.imread(url)
    
    # 2. Preprocess image
    # Convert BGR to RGB (OpenCV uses BGR by default, but check if io.imread is RGB)
    cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    # Blur to reduce noise
    img=cv2.blur(img,(5,5))
    # Threshold to convert to binary (black & white)
    retval,img=cv2.threshold(img,210,255,cv2.THRESH_BINARY)
    # Resize to match model input size (24x24)
    img=cv2.resize(img,(24,24))
    # Second threshold (redundant but ensures binary?)
    retval,img=cv2.threshold(img,210,255,cv2.THRESH_BINARY)
    # Flatten image to 1D array
    image_as_array=numpy.ndarray.flatten(numpy.array(img))
    
    # Optional: Scale data if scaler was used
    #image_as_array=scaler.transform(image_as_array)
    
    # 3. Predict direction
    result=alg.predict([image_as_array])[0]
    
    # 4. Send command to Arduino
    if result=='forward':
        s.write(b'f')
        # Wait slightly to prevent flooding commands
        time.sleep(1)
    elif result=='right':
        s.write(b'r')
        time.sleep(1)
    elif result=='left':
        s.write(b'l')
        time.sleep(1)
    
    # Pause before next iteration
    time.sleep(1)
    print(result)
    
    # Recursive call to continue driving loop
    drive()

print("Start Driving")
drive()
# Close serial connection (this line is rarely reached due to infinite recursion)
s.close()