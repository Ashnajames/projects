# -*- coding: utf-8 -*-
"""AA5 NEW.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1o0Cuj_7BaXtciGwWaAOyV8_vD2BBSp1o
"""

import zipfile

# Replace 'your_dataset.zip' with the actual ZIP file name
with zipfile.ZipFile('archive (7).zip', 'r') as zip_ref:
    zip_ref.extractall('dataset_directory')

import os
import cv2
import numpy as np
from PIL import Image

# Define the path to the directory containing the extracted dataset
dataset_directory = 'dataset_directory'  # Replace with the actual directory path

# Define the target image size (e.g., 28x28 pixels)
image_size = (28, 28)

# Initialize lists to store images and labels
all_images = []
all_labels = []

# Iterate through the subdirectories (folders)
for digit_folder in os.listdir(dataset_directory):
    # Create the full path to the digit folder
    digit_folder_path = os.path.join(dataset_directory, digit_folder)

    # Check if it's a directory
    if os.path.isdir(digit_folder_path):
        # Get the digit label from the folder name
        label = int(digit_folder)

        # Initialize lists to store images and labels for this digit
        digit_images = []
        digit_labels = []

        # Iterate through the files (images) in the current digit folder
        for filename in os.listdir(digit_folder_path):
            if filename.endswith(".png") or filename.endswith(".jpeg") or filename.endswith(".jpg"):
                # Load the image using PIL (handles both PNG and JPEG)
                image = Image.open(os.path.join(digit_folder_path, filename)).convert('L')
                image = image.resize(image_size, Image.ANTIALIAS)
                image = np.array(image)

                # Normalize pixel values to the range [0, 1]
                image = image.astype("float32") / 255.0

                # Append the image and label to the digit-specific lists
                digit_images.append(image)
                digit_labels.append(label)

        # Convert the digit-specific lists to NumPy arrays and append to the overall lists
        digit_images = np.array(digit_images)
        digit_labels = np.array(digit_labels)

        all_images.append(digit_images)
        all_labels.append(digit_labels)

# Convert the overall lists to NumPy arrays
all_images = np.concatenate(all_images, axis=0)
all_labels = np.concatenate(all_labels, axis=0)

# Check the shape of the arrays (should be (num_samples, height, width))
print("Shape of images array:", all_images.shape)
print("Shape of labels array:", all_labels.shape)

from sklearn.model_selection import train_test_split

# Split the dataset into training (70%) and the remaining data (30%)
train_images, remaining_images, train_labels, remaining_labels = train_test_split(
    all_images, all_labels, test_size=0.3, random_state=42)

# Split the remaining data into validation (50%) and test (50%)
validation_images, test_images, validation_labels, test_labels = train_test_split(
    remaining_images, remaining_labels, test_size=0.5, random_state=42)

# Print the shapes of the resulting sets
print("Training set:")
print("Images shape:", train_images.shape)
print("Labels shape:", train_labels.shape)

print("\nValidation set:")
print("Images shape:", validation_images.shape)
print("Labels shape:", validation_labels.shape)

print("\nTest set:")
print("Images shape:", test_images.shape)
print("Labels shape:", test_labels.shape)

import os

# Replace 'file_path' with the path to your file
file_path = 'dataset_dictionary'  # Replace with your file path

# Get the file extension using os.path.splitext()
file_extension = os.path.splitext(file_path)[-1].lower()

# Print the file extension
print("File Extension:", file_extension)







import os
import numpy as np

# Define the path to the directory containing the extracted dataset
dataset_directory = 'dataset_directory'  # Replace with the actual directory path

# Initialize lists to store image names and their labels
image_names = []
labels = []

# Iterate through the subdirectories (folders)
for digit_folder in os.listdir(dataset_directory):
    # Create the full path to the digit folder
    digit_folder_path = os.path.join(dataset_directory, digit_folder)

    # Check if it's a directory
    if os.path.isdir(digit_folder_path):
        # Get the digit label from the folder name (e.g., "zero_full" -> 0)
        label = int(digit_folder.split('_')[0])

        # Iterate through the files (images) in the current digit folder
        for filename in os.listdir(digit_folder_path):
            if filename.endswith(".png") or filename.endswith(".jpeg") or filename.endswith(".jpg"):
                # Append the image name and label to the respective lists
                image_names.append(filename)
                labels.append(label)

# Convert the lists of image names and labels to NumPy arrays
image_names = np.array(image_names)
labels = np.array(labels)

# Print the original labels (from image names) and their corresponding labels
for original_label, corresponding_label in zip(image_names, labels):
    print(f"Original Label: {original_label}, Corresponding Label: {corresponding_label}")

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# Define the CNN model
model = keras.Sequential([
    # Convolutional layer 1
    layers.Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(28, 28, 1)),
    layers.MaxPooling2D(pool_size=(2, 2)),

    # Convolutional layer 2
    layers.Conv2D(64, kernel_size=(3, 3), activation='relu'),
    layers.MaxPooling2D(pool_size=(2, 2)),

    # Flatten the output from convolutional layers
    layers.Flatten(),

    # Fully connected (dense) layers
    layers.Dense(128, activation='relu'),
    layers.Dense(10, activation='softmax')  # Output layer with 10 classes (0-9)
])

# Compile the model
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Display the model summary
model.summary()

# Assume you've already preprocessed the data and have train_images, train_labels,
# validation_images, validation_labels, test_images, and test_labels

# Define the number of training epochs and batch size
epochs = 10
batch_size = 64

# Train the model
history = model.fit(
    train_images, train_labels,
    epochs=epochs,
    batch_size=batch_size,
    validation_data=(validation_images, validation_labels),
    verbose=2  # You can set the verbosity level as needed
)

# Evaluate the model on the test set
test_loss, test_accuracy = model.evaluate(test_images, test_labels, verbose=2)

print(f"Test Accuracy: {test_accuracy * 100:.2f}%")

import numpy as np
from sklearn.metrics import confusion_matrix, classification_report
import matplotlib.pyplot as plt

# Use the trained model to make predictions on the test data
predictions = model.predict(test_images)

# Convert one-hot encoded predictions to class labels (0 to 9)
predicted_labels = np.argmax(predictions, axis=1)

# Calculate the confusion matrix
conf_matrix = confusion_matrix(test_labels, predicted_labels)

# Print the confusion matrix
print("Confusion Matrix:")
print(conf_matrix)

# Generate a classification report
class_report = classification_report(test_labels, predicted_labels, target_names=[str(i) for i in range(10)])

# Print the classification report
print("\nClassification Report:")
print(class_report)

# Calculate and display accuracy
accuracy = np.sum(np.diagonal(conf_matrix)) / np.sum(conf_matrix)
print(f"\nAccuracy: {accuracy * 100:.2f}%")

# Visualize the confusion matrix as a heatmap
plt.figure(figsize=(8, 6))
plt.imshow(conf_matrix, interpolation='nearest', cmap=plt.get_cmap('Blues'))
plt.title('Confusion Matrix')
plt.colorbar()
plt.xlabel('Predicted')
plt.ylabel('True')
plt.xticks(np.arange(10), [str(i) for i in range(10)])
plt.yticks(np.arange(10), [str(i) for i in range(10)])
plt.show()

import os
import numpy as np
import pandas as pd
from PIL import Image
from google.colab import drive

# Mount Google Drive to access images
drive.mount('/content/drive')

# Define the path to the directory containing your images in Google Drive
drive_image_directory = '/content/drive/My Drive/AAAAAA/numbers'  # Replace with your actual folder path

# Initialize lists to store image names and image data
image_names = []
image_data = []

# Iterate through the files in the image directory
for filename in os.listdir(drive_image_directory):
    if filename.endswith(".png") or filename.endswith(".jpeg") or filename.endswith(".jpg"):
        # Load and preprocess the image
        image_path = os.path.join(drive_image_directory, filename)
        image = Image.open(image_path).convert('L')  # Convert to grayscale if needed
        image = image.resize((28, 28), Image.ANTIALIAS)
        image = np.array(image).astype("float32") / 255.0

        # Append the image name and data to the respective lists
        image_names.append(filename)
        image_data.append(image)

# Convert image_data to a NumPy array
image_data = np.array(image_data)

# Use the trained model to make predictions
predictions = model.predict(image_data)
predicted_labels = np.argmax(predictions, axis=1)

# Create a DataFrame with image names and predicted labels
results_df = pd.DataFrame({'Image Name': image_names, 'Predicted Label': predicted_labels})

# Define the path where you want to save the results Excel file in Google Drive
results_file_path = '/content/drive/My Drive/AAAAAA/numbers/AA.xlsx'  # Replace with your desired path

# Save the results to an Excel file
results_df.to_excel(results_file_path, index=False)

# Unmount Google Drive
drive.flush_and_unmount()

print(f"Predictions saved to: {results_file_path}")

























