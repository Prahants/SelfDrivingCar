import numpy
from os import listdir
from os.path import isfile,join
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import cv2

# Initialize lists for data (x) and labels (y)
x = []
y = []

# Get list of all image files in the 'testsdc' directory
files_name = [f for f in listdir('testsdc') if isfile(join('testsdc', f))]

# Loop through each image file to preprocess and load data
for name in files_name:
    # Read the image
    img = cv2.imread(join('testsdc', name))
    
    # Apply blur to reduce noise
    img = cv2.blur(img, (5, 5))
    
    # Apply binary thresholding to convert to black and white
    retval, img = cv2.threshold(img, 201, 255, cv2.THRESH_BINARY)
    
    # Resize image to 24x24 pixels to match input size
    img = cv2.resize(img, (24, 24))
    
    # Flatten the image array to a 1D array for the classifier
    image_as_array = numpy.ndarray.flatten(numpy.array(img))
    
    # Append the flattened image to data list
    x.append(image_as_array)
    
    # Extract label from filename (e.g., 'forward_1.jpg' -> 'forward')
    y.append(name.split('_')[0])

# Split data into training (80%) and testing (20%) sets
xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.2, random_state=42)

# Initialize StandardScaler to normalize the data
scaler = StandardScaler()
# Fit the scaler on training data
scaler.fit(xtrain)
# Transform both training and testing data
xtrain = scaler.transform(xtrain)
xtest = scaler.transform(xtest)

# Initialize MLPClassifier (Neural Network)
# solver='lbfgs': optimizer in the family of quasi-Newton methods
# alpha=100.0: L2 penalty (regularization term) parameter
# hidden_layer_sizes=50: single hidden layer with 50 neurons
alg = MLPClassifier(solver='lbfgs', alpha=100.0, random_state=1, hidden_layer_sizes=50)

# Train the model
alg.fit(xtrain, ytrain)

# Print the accuracy score on the test set
print("Model Accuracy:", alg.score(xtest, ytest))
    
