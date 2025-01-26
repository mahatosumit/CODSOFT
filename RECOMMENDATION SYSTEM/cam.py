import os
import h5py
import tensorflow as tf

# Disable oneDNN optimizations
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

# Check if the file exists and is valid
file_path = "./model6.h5"

try:
    # Verify file existence and integrity
    with h5py.File(file_path, 'r') as f:
        print("HDF5 file is valid. Keys:", list(f.keys()))

    # Attempt to load the model
    model = tf.keras.models.load_model(file_path, compile=False)
    print("Model loaded successfully!")
    
    # Convert to TFLite
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()

    # Save the converted model
    with open("model.tflite", "wb") as f:
        f.write(tflite_model)
    print("Model converted and saved as 'model.tflite'.")
except FileNotFoundError:
    print(f"Error: File not found at path {file_path}")
except OSError as e:
    print(f"Error with the file: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
