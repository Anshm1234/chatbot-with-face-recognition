import tensorflow as tf
import os

tf.keras.backend.clear_session()  # Clears any cached model data

# Delete any old saved models
if os.path.exists("chat_model.h5"):
    os.remove("chat_model.h5")

if os.path.exists("tokenizer.pkl"):
    os.remove("tokenizer.pkl")

if os.path.exists("label_encoder.pkl"):
    os.remove("label_encoder.pkl")

print("Old models deleted. Ready for retraining!")
