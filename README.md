# 🔐 Security Chatbot with Face Recognition

This project integrates **face recognition** with a **voice-enabled chatbot** to provide a secure and intelligent interaction system. It first verifies the user through facial recognition and then enables voice-based command processing through a chatbot trained on custom intents.

---

## 📌 Features

- ✅ **Face Recognition**
  - Recognizes authorized users using OpenCV and face encodings.
  - Displays a "Proceed" button only for verified individuals.

- 🧠 **AI-Powered Chatbot**
  - NLP-based intent classification trained using TensorFlow.
  - Uses speech-to-text and text-to-speech for full voice interaction.

- 🔐 **Security First**
  - No access to chatbot unless the face is recognized.
  - Can be extended for security systems or smart access control.

---

## 🛠️ Tech Stack

- **Face Detection**: OpenCV, `face_recognition`
- **Chatbot/NLP**: TensorFlow, NLTK
- **Speech**: `speech_recognition`, `pyttsx3`
- **Language**: Python
- **Optional GUI**: Tkinter

---

## 📁 Project Structure

security_chatbot/
├── chatbot.py # Chatbot logic and speech handling
├── face_recognition.py # Face detection and recognition
├── generate_encodings.py # Generates encodings from dataset
├── encodings.pickle # Stored face encodings
├── chat_model.h5 # Trained model for intent classification
├── intents.json # Dataset of intents for chatbot
├── main.py # Main driver combining face + chatbot
├── dataset/ # Face image dataset for users
├── requirements.txt # Dependencies
└── README.md # Documentation

yaml
Copy
Edit

---

## 🚀 Getting Started

### 🔧 Prerequisites

Install the dependencies:

```bash
pip install -r requirements.txt
Also install and configure:

FFmpeg: https://ffmpeg.org/download.html

Add ffmpeg/bin to your system PATH (required for TTS/speech)

▶️ How to Run
bash
Copy
Edit
python main.py
Steps:

Opens webcam for face recognition.

If recognized, launches the voice-based chatbot.

🧠 Training the Chatbot
To retrain the intent model:

bash
Copy
Edit
python train_chatbot.py
Make sure intents.json is formatted like:

json
Copy
Edit
{
  "intents": [
    {
      "tag": "greeting",
      "patterns": ["Hello", "Hi there"],
      "responses": ["Hi!", "Hello, how can I help you?"]
    }
  ]
}
🧑 Adding a New Face
Add 5+ images of a new user in:
dataset/<username>/

Generate encodings:

bash
Copy
Edit
python generate_encodings.py
This updates encodings.pickle for recognition.

📷 Screenshots
Add your screenshots here (optional):

Recognized face ➜ Proceed

Chatbot voice interaction in terminal or GUI

🔐 Use Cases
Home or Office Security Systems

Secure Smart Assistants

Personalized Voice Interface

✅ Future Ideas
Emotion detection from face

Admin panel to add/remove users

Real-time logging of interactions

👨‍💻 Author
Ansh Madaan
Engineering Student & AI Developer 
