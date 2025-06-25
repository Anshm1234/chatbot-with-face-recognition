import cv2
import numpy as np
import face_recognition
import os
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load known faces and their names
known_face_encodings = []
known_face_names = []

def encode_multiple_images(image_paths):
    encodings = []
    for img_path in image_paths:
        logging.info(f"Processing image: {img_path}")
        
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)  # Load as grayscale
        if img is None:
            logging.error(f"Failed to load image: {img_path}")
            continue
        
        if img.dtype != np.uint8:
            logging.error(f"Image {img_path} is not 8-bit. Found dtype: {img.dtype}")
            continue
        
        # Convert grayscale to RGB explicitly ensuring it's in correct format
        rgb_img = cv2.merge([img, img, img])  # Convert grayscale to 3-channel RGB
        rgb_img = np.ascontiguousarray(rgb_img, dtype=np.uint8)  # Ensure 8-bit format
        
        logging.info(f"Converted image shape: {rgb_img.shape}, dtype: {rgb_img.dtype}")
        
        face_enc = face_recognition.face_encodings(rgb_img)
        if face_enc:
            encodings.append(face_enc[0])
        else:
            logging.warning(f"No face found in image: {img_path}")

    return np.mean(encodings, axis=0) if encodings else None

# Load dataset dynamically from "face_dataset" folder
dataset_path = "../face_dataset"
if not os.path.exists(dataset_path):
    logging.error(f"Dataset folder not found: {dataset_path}")
else:
    for person_name in os.listdir(dataset_path):
        person_folder = os.path.join(dataset_path, person_name)
        if os.path.isdir(person_folder):
            image_paths = [os.path.join(person_folder, img) for img in os.listdir(person_folder) if img.endswith(('.jpg', '.png'))]
            encoding = encode_multiple_images(image_paths)
            if encoding is not None:
                known_face_encodings.append(encoding)
                known_face_names.append(person_name)
            else:
                logging.warning(f"No valid encodings for {person_name}")

# Initialize webcam
video_capture = cv2.VideoCapture(0)
if not video_capture.isOpened():
    logging.error("Failed to open webcam.")
    exit()

while True:
    ret, frame = video_capture.read()
    if not ret:
        logging.warning("Failed to capture frame from webcam.")
        continue
    
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        face_distance = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distance) if len(face_distance) > 0 else None

        if best_match_index is not None and face_distance[best_match_index] < 0.4:
            name = known_face_names[best_match_index]
            color = (0, 255, 0)
            button_text = "Proceed"
            time.sleep(5000)
        else:
            name = "Unknown"
            color = (0, 0, 255)
            button_text = ""

        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

        if button_text:
            cv2.rectangle(frame, (50, 400), (200, 450), (0, 255, 0), -1)
            cv2.putText(frame, button_text, (70, 435), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    cv2.imshow("Face Recognition", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
