import json
import pickle
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential # type: ignore
from tensorflow.keras.layers import Dense, Embedding, GlobalAveragePooling1D # type: ignore
from tensorflow.keras.preprocessing.text import Tokenizer # type: ignore
from tensorflow.keras.preprocessing.sequence import pad_sequences # type: ignore
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split  # Import train_test_split

# Load JSON file
file_path = r"D:\4th semester\cognitive\project\security_chatbot\commands.json"
with open(file_path, "r") as file:
    data = json.load(file)

training_sentences = []
training_labels = []
labels = []
responses = []

for intent in data['commands']:
    for pattern in intent['patterns']:
        training_sentences.append(pattern)
        training_labels.append(intent['tag'])
    responses.append(intent['responses'])

    if intent['tag'] not in labels:
        labels.append(intent['tag'])

number_of_classes = len(labels)
print("Total Classes:", number_of_classes)

# Encode Labels
label_encoder = LabelEncoder()
training_labels = label_encoder.fit_transform(training_labels)

# Tokenization
vocab_size = 1000
max_len = 20
oov_token = "<OOV>"
embedding_dim = 16

tokenizer = Tokenizer(num_words=vocab_size, oov_token=oov_token)
tokenizer.fit_on_texts(training_sentences)
word_index = tokenizer.word_index
sequences = tokenizer.texts_to_sequences(training_sentences)
padded_sequences = pad_sequences(sequences, truncating='post', maxlen=max_len)

# 🔹 Split Data into Training and Validation Sets
X_train, X_val, y_train, y_val = train_test_split(
    padded_sequences, training_labels, test_size=0.2, random_state=42
)

# Model Architecture
model = Sequential([
    Embedding(vocab_size, embedding_dim, input_length=max_len),
    GlobalAveragePooling1D(),
    Dense(16, activation="relu"),
    Dense(16, activation="relu"),
    Dense(number_of_classes, activation="softmax")
])

# Compile Model
model.compile(loss='sparse_categorical_crossentropy', optimizer="adam", metrics=["accuracy"])

# Train Model with Validation Data
history = model.fit(X_train, np.array(y_train), 
                    epochs=550,  # Reduce epochs for better analysis
                    validation_data=(X_val, np.array(y_val)))

# Save Model and Tokenizer
model.save("chat_model.h5")

with open("tokenizer.pkl", "wb") as f:
    pickle.dump(tokenizer, f, protocol=pickle.HIGHEST_PROTOCOL)

with open("label_encoder.pkl", "wb") as encoder_file:
    pickle.dump(label_encoder, encoder_file, protocol=pickle.HIGHEST_PROTOCOL)

# 🔹 Plot Accuracy and Loss Graphs
plt.figure(figsize=(8, 4))

# Accuracy Plot
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.title('Training vs. Validation Accuracy')
plt.grid()

# Loss Plot
plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.title('Training vs. Validation Loss')
plt.grid()

# Show Plots
plt.show()
