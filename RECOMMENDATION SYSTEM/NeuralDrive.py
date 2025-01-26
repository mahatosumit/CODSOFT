import cv2
import numpy as np
from tensorflow.keras.models import load_model
import time

class NeuralDriver:
    def __init__(self, model_path=r'/home/pi/Documents/ADAS/ADAS_CODE/model.h5'):
        """Initialize NeuralDriver with the pre-trained model."""
        try:
            self.model = load_model(model_path)
            print(f"Model loaded successfully from {model_path}")
        except Exception as e:
            raise RuntimeError(f"Failed to load model from {model_path}. Error: {str(e)}")
        
        self.steering_sensitivity = 0.70
        self.max_throttle = 0.22

    def preprocess_image(self, img):
        """Preprocess the input image for the neural network."""
        try:
            img = cv2.resize(img, (240, 120))
            img = img[54:120, :, :]  # Crop to focus on the road
            img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
            img = cv2.GaussianBlur(img, (3, 3), 0)
            img = cv2.resize(img, (200, 66))  # Model-specific input shape
            img = img / 255.0  # Normalize pixel values
            return img
        except Exception as e:
            print(f"Image preprocessing error: {str(e)}")
            return None

    def predict_steering(self, frame):
        """Predict steering angle and throttle from the input frame."""
        try:
            processed = self.preprocess_image(frame)
            if processed is None:
                raise ValueError("Processed image is None.")
            
            processed = np.expand_dims(processed, axis=0)  # Add batch dimension
            steering = float(self.model.predict(processed, verbose=0))  # Suppress logging
            return steering * self.steering_sensitivity, self.max_throttle
        except Exception as e:
            print(f"Prediction error: {str(e)}")
            return 0.0, 0.0

def test():
    """Test the neural driver using webcam input."""
    cap = cv2.VideoCapture(0)  # Use default camera
    if not cap.isOpened():
        print("Error: Cannot access the camera.")
        return

    driver = None
    try:
        driver = NeuralDriver()
    except RuntimeError as e:
        print(e)
        return

    prev_time = time.time()
    frame_count = 0

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Cannot read from the camera.")
                break
            
            # Predict steering and throttle
            steering, throttle = driver.predict_steering(frame)
            print(f"Steering: {steering:.2f}, Throttle: {throttle:.2f}")
            
            # Display frame with overlay
            cv2.putText(frame, f"Steering: {steering:.2f}", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # FPS calculation and display
            frame_count += 1
            current_time = time.time()
            elapsed_time = current_time - prev_time
            if elapsed_time >= 1.0:
                fps = frame_count / elapsed_time
                frame_count = 0
                prev_time = current_time
                cv2.putText(frame, f"FPS: {fps:.2f}", (10, 70), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            
            cv2.imshow('Neural Drive Test', frame)
            
            # Break loop on 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("Resources released. Exiting...")

if __name__ == '__main__':
    test()
