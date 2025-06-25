import os
import pickle
import face_recognition
from PIL import Image
import numpy as np
import cv2

def generate_encodings(dataset_folder="face_dataset", encoding_file="encodings.pkl"):
    """
    Processes images from the dataset and computes face encodings.
    The dataset folder should be structured as:
        face_dataset/
            PersonName/
                image1.jpg, image2.jpg, ...
    Encodings are saved in a pickle file as a dictionary with keys:
        "encodings" -> list of face encodings
        "names"     -> corresponding person names
    """
    known_encodings = []
    known_names = []
    
    # Process only common image file extensions
    valid_extensions = (".jpg", ".jpeg", ".png")
    
    for person_name in os.listdir(dataset_folder):
        person_path = os.path.join(dataset_folder, person_name)
        if not os.path.isdir(person_path):
            continue

        for image_name in os.listdir(person_path):
            if not image_name.lower().endswith(valid_extensions):
                continue

            image_path = os.path.join(person_path, image_name)
            try:
                # Open image with PIL and convert to RGB (8-bit per channel)
                img = Image.open(image_path).convert("RGB")
                # Convert to a contiguous NumPy array with explicit dtype uint8
                rgb_img = np.ascontiguousarray(np.array(img, dtype=np.uint8))
            except Exception as e:
                print(f"Error reading image {image_path} with PIL: {e}")
                continue

            # Debug: print image shape and dtype
            print(f"Processing {image_path}: shape={rgb_img.shape}, dtype={rgb_img.dtype}")
            
            # Check that image has 3 channels (RGB)
            if len(rgb_img.shape) != 3 or rgb_img.shape[2] != 3:
                print(f"Skipping {image_path}: not a valid RGB image.")
                continue
            
            # If the image is too small, upscale it (e.g., to 250x250)
            if rgb_img.shape[0] < 250 or rgb_img.shape[1] < 250:
                print(f"Image {image_path} is too small ({rgb_img.shape}), upscaling to (250,250).")
                rgb_img = cv2.resize(rgb_img, (250, 250))
                print(f"New shape: {rgb_img.shape}")

            # Compute face encodings
            try:
                encodings = face_recognition.face_encodings(rgb_img)
            except Exception as e:
                print(f"Error processing {image_path}: {e}")
                continue

            if encodings:
                known_encodings.append(encodings[0])
                known_names.append(person_name)
            else:
                print(f"Warning: No face detected in image: {image_path}")

    data = {"encodings": known_encodings, "names": known_names}
    with open(encoding_file, "wb") as f:
        pickle.dump(data, f)
    print(f"Encodings saved to {encoding_file}")

if __name__ == "__main__":
    generate_encodings()
