import cv2
import os
import time

def capture_faces(output_folder="face_dataset", frame_skip=5, wait_time=0.3, target_size=(250, 250)):
    """
    Captures face images from the webcam, saves them under a folder named after the person,
    and then exits when 'q' is pressed.

    Parameters:
    - output_folder: Directory to save images.
    - frame_skip: Number of frames to skip between processing.
    - wait_time: Minimum time (in seconds) between saved images.
    - target_size: Tuple (width, height) to which the face image is resized.
    """
    person_name = input("Enter the person's name: ").strip()
    if not person_name:
        print("Error: Name cannot be empty.")
        return

    person_folder = os.path.join(output_folder, person_name)
    os.makedirs(person_folder, exist_ok=True)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Unable to open webcam")
        return

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    frame_count = 0
    saved_count = 0
    last_save_time = time.time()

    print("Capturing images... Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to read frame from webcam.")
            break

        frame_count += 1
        if frame_count % frame_skip != 0:
            continue

        # Convert to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))

        for (x, y, w, h) in faces:
            # Draw rectangle for visual feedback
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            if time.time() - last_save_time >= wait_time:
                # Crop the face region from the original color frame
                face_img = frame[y:y+h, x:x+w]
                # Resize to the target size (e.g., 250x250) for better resolution
                face_img = cv2.resize(face_img, target_size)
                img_path = os.path.join(person_folder, f"{person_name}_{saved_count:04d}.jpg")
                cv2.imwrite(img_path, face_img)
                print(f"Saved: {img_path}")
                saved_count += 1
                last_save_time = time.time()

        cv2.imshow(f"Capturing for {person_name} (Press 'q' to quit)", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"Capture complete! {saved_count} images saved for '{person_name}'.")

if __name__ == "__main__":
    capture_faces()
