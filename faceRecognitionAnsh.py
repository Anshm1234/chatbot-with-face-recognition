import csv
import datetime
import cv2
import pickle
import face_recognition
import numpy as np
from sklearn.neighbors import KDTree
import tkinter as tk
from tkinter import messagebox
from chatbot import final, speak  # Ensure this imports your chatbot's final function
import pyttsx3 as py



recognized_name = None
proceed_button = None

root = tk.Tk()
# root.title("Chatbot")
# root.geometry("500x250")
# root.resizable(False, False)

def load_encodings(encoding_file="encodings.pkl"):
    """Loads the saved face encodings from the pickle file."""
    with open(encoding_file, "rb") as f:
        data = pickle.load(f)
    return data

def build_kd_tree(encodings):
    """Builds a KD-Tree for efficient nearest neighbor search."""
    return KDTree(encodings, metric='euclidean')

def recognize_faces(encoding_file="encodings.pkl", video_source=0, tolerance=0.4, frame_skip=5):
    """
    Runs real-time face recognition using the webcam.
    Matches faces against the known encodings loaded from the pickle file.
    Displays a 'Proceed' button when an authorized face is detected.
    """
    data = load_encodings(encoding_file)
    known_encodings = np.array(data["encodings"])
    known_names = data["names"]

    # Build KD-Tree
    tree = build_kd_tree(known_encodings)

    cap = cv2.VideoCapture(video_source)
    if not cap.isOpened():
        print("Error: Unable to open webcam")
        return

    # Set up the Tkinter root window
    root = tk.Tk()
    root.title("Chatbot")  # Set the window title
    root.geometry("500x250")  # Set the window size
    root.resizable(False, False)  # Disable window resizing

    # Create a label to display instructions
    label = tk.Label(root, text="Waiting for authorized face...", font=("Helvetica", 16))
    label.pack(pady=20)

    frame_count = 0
    recognized_names = set()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to read frame from webcam.")
            break

        frame_count += 1
        if frame_count % frame_skip != 0:
            continue

        # Convert from BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # Search for the nearest neighbor in the KD-Tree
            dist, ind = tree.query([face_encoding], k=1)
            if dist[0][0] <= tolerance:
                name = known_names[ind[0][0]]
                global recognized_name
                recognized_name = name 
                color = (0, 255, 0)  # Green for known faces
                if name not in recognized_names:
                    recognized_names.add(name)
                    # Update the label text
                    label.config(text=f"Authorized face detected: {name}")
                    # Create and pack the 'Proceed' button
                    show_proceed_button = tk.Button(root, text="Proceed", command=lambda: show_proceed_button(cap, root))
                    show_proceed_button.pack(pady=20)
            else:
                name = "Unknown"
                color = (0, 0, 255)  # Red for unknown faces

            # Draw a rectangle around the face
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            # Draw the label below the face
            cv2.putText(frame, name, (left, bottom + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)

        # Display the frame in a window
        cv2.imshow("Face Recognition", frame)

        # Update the Tkinter window
        root.update_idletasks()
        root.update()

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Face recognition stopped.") 

if __name__ == "__main__":
    recognize_faces() 