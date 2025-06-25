import json
import pickle
from tensorflow.keras.models import load_model # type: ignore
from tensorflow.keras.preprocessing.sequence import pad_sequences # type: ignore
import random
import numpy as np

file_path = r"D:\4th semester\cognitive\project\security_chatbot\commands.json"
with open(file_path, "r") as file:
    data = json.load(file)

model = load_model("chat_model.h5")

with open("tokenizer.pkl", "rb") as f:
    tokenizer=pickle.load(f)

with open("label_encoder.pkl", "rb") as encoder_file:
    label_encoder=pickle.load(encoder_file)

while True:
    input_text = input("Enter your command-> ")
    padded_sequences = pad_sequences(tokenizer.texts_to_sequences([input_text]), maxlen=20, truncating='post')
    result = model.predict(padded_sequences)
    tag = label_encoder.inverse_transform([np.argmax(result)])

    for i in data['commands']:
        if i['tag'] == tag:
            print(np.random.choice(i['responses']))
