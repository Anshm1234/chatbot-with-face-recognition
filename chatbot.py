import pyttsx3 as py
import  speech_recognition as sr
import datetime
import time 
import webbrowser
import pyautogui
import sys
import os
import subprocess
import json
import pickle
from tensorflow.keras.models import load_model # type: ignore
from tensorflow.keras.preprocessing.sequence import pad_sequences # type: ignore
import random
import numpy as np
import psutil
import asyncio
from shazamio import Shazam
from pydub import AudioSegment
AudioSegment.converter = r"C:\path\to\ffmpeg.exe"


file_path = r"D:\4th semester\cognitive\project\security_chatbot\commands.json"
with open(file_path, "r") as file:
    data = json.load(file)

model = load_model("chat_model.h5")

with open("tokenizer.pkl", "rb") as f:
    tokenizer=pickle.load(f)

with open("label_encoder.pkl", "rb") as encoder_file:
    label_encoder=pickle.load(encoder_file)

async def recognize_song():
    shazam = Shazam()
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Reduce background noise
        recognizer.energy_threshold = 100  # Ensure low-volume sounds are captured
        recognizer.dynamic_energy_threshold = False  # Prevent auto-adjustment

        print("Listening to the song snippet... Speak now!")
        audio = recognizer.listen(source, phrase_time_limit=10)  # Capture for 10 sec

        with open("song_sample.wav", "wb") as f:
            f.write(audio.get_wav_data(convert_rate=44100))  # Save with high quality

    print(" Recognizing the song, please wait...")

    if os.path.exists("song_sample.wav"):
        print("Audio file saved successfully!")

        result = await shazam.recognize("song_sample.wav")

    if result.get('matches'):
        song = result['track'].get('title', 'Unknown')
        artist = result['track'].get('subtitle', 'Unknown')
        url = result['track'].get('url', 'No link available')

        print(f" Song: {song} - {artist}")
        speak(f"it's {song} by {artist}")
        print(f" Listen here: {url}")
        return f"The song is {song} by {artist}. You can listen to it here: {url}"
    else:
        return "Sorry, I couldn't recognize the song."



def initialize_engine():
    engine = py.init("sapi5")  # Initialize text-to-speech
    
    voices = engine.getProperty('voices')  
    engine.setProperty('voice', voices[1].id)  # Choose a female voice (update index if needed)

    engine.setProperty('rate', 130)  # Adjust speed for a smoother voice
    engine.setProperty('volume', 1.0)  # Slightly high volume for clarity
    
    return engine

def speak(text):
    engine=initialize_engine()
    engine.say(text)
    engine.runAndWait()

def initialize_engine_for_exit():
    engine = py.init("sapi5")  # Initialize text-to-speech
    
    voices = engine.getProperty('voices')  
    engine.setProperty('voice', voices[0].id)  # Choose a female voice (update index if needed)

    engine.setProperty('rate', 130)  # Adjust speed for a smoother voice
    engine.setProperty('volume', 1.0)  # Slightly high volume for clarity
    
    return engine

def speak_for_exit(text):
    engine=initialize_engine_for_exit()
    time.sleep(0.5)
    engine.say(text)
    engine.runAndWait()

def command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source,duration=0.5)
        print("Listening....", end="" ,flush=True)
        r.pause_threshold=1.0
        r.phrase_threshold=0.3
        r.sample_rate=48000
        r.dynamic_energy_threshold=True
        r.operation_timeout=5
        r.non_speaking_duration=0.5
        r.dynamic_energy_adjustment=2
        r.energy_threshold=4000
        r.phrase_time_limit=10
        audio=r.listen(source)
    try:
        print("\r",end="",flush=True)
        print("Recognizing......", end="" , flush=True)
        print("\r",end="",flush=True)
        query = r.recognize_google(audio)
        print(f"User said :{query}\n")
    except Exception as e:
        print("Soory can you say that again please")
        speak("Soory can you say that again please")
        return "None"
    return query

def wishme():
    hour=int(datetime.datetime.now().hour)
    t=time.strftime("%I:%M:%p")
    if(hour>=5) and (hour<=11) and ('AM' in t):
        speak(f"HI Good Morning ,How can i help you")
    elif(hour>=12) and (hour<=17) and ('PM' in t):
        speak("HI Good Afternoon sir,How can i help you")
    elif(hour>=18) and (hour<=20) and ('PM' in t):
        speak("HI Good Evening sir,How can i help you")
    else:
        speak(f"Its {hour} at night is there something i can do for you ")

def social_media(command):
    if 'open facebook' in command:
        speak("Opening Facebook")
        webbrowser.open("https://www.facebook.com/")
    elif 'open discord' in command:
        speak("Opening Discord")
        webbrowser.open("https://discord.com/")
    elif 'open whatsapp' in command:
        speak("Opening Whatsapp")
        webbrowser.open("https://web.whatsapp.com/")
    elif ('open phub' in command) or ('p hub' in command):
        print("Harsh is a minor ,dont spoil him")
        speak("Harsh is a minor ,dont spoil him")
    elif 'open instagram' in command:
        speak("Opening instagram")
        webbrowser.open("https://www.instagram.com")
    elif 'close facebook' in command:
        speak("closing Facebook")
        close_website("Facebook")
    elif 'close whatsapp' in command:
        speak("closing whatsapp")
        close_website("whatsapp")
    elif 'close discord' in command:
        speak("closing discord")
        close_website("discord")
    elif 'close Instagram' in command:
        speak("closing Instagram")
        close_website("Instagram")    
    else:
        speak("no results found")   

def close_website(site):
    os.system("taskkill /F /IM msedge.exe")  

def openapp(command):
    if "calculator" in command:
        speak("opening calculator")
        os.startfile('C:\\Windows\\System32\\calc.exe')
    elif "notepad" in command:
        speak("opening notepad")
        os.startfile('C:\\Windows\\System32\\notepad.exe')
        open_notepad()

def closeapp(command):
    if "calculator" in command:
        speak("closing calculator")
        os.system('taskkill /f /im calc.exe')
    elif "notepad" in command:
        speak("closing notepad")
        os.system('taskkill /f /im notepad.exe')

def browsing(query):
    if 'open google' in query:
        speak("what do you want to search....")
        s = command()
        webbrowser.open(f"{s}")
    elif 'close google' in query:
        speak("closing google")
        close_website("google")
              
def condition():
    usage=str(psutil.cpu_percent())
    speak(f"CPU is at {usage} percentage")
    battery=psutil.sensors_battery()
    percentage=battery.percent
    speak(f"our system have {percentage} battery")

    if percentage<20:
        speak("connect your charger, am gonna die")

def open_notepad():
    speak("Do you want to open an existing file or create a new one?")
    choice = command().lower()

    if "new" in choice:
        speak("What should be the name of the new file?")
        filename = command().strip() + ".txt"
        file_path = os.path.join(os.getcwd(), filename)

        # Create the file first and open it
        with open(file_path, "w") as file:
            pass  # Just creating the empty file
        
        # Open Notepad
        os.startfile(file_path)  
        speak("File created and opened. What do you want to write?")
        time.sleep(2)  # Give some time for Notepad to open

        content = command()  # Take user input for content

        with open(file_path, "w") as file:
            file.write(content)
        
        speak("Content written successfully.")

    elif "existing" in choice:
        speak("Please say the name of the file you want to open.")
        filename = command().strip() + ".txt"
        file_path = os.path.join(os.getcwd(), filename)

        if os.path.exists(file_path):
            os.startfile(file_path)
            speak("File opened. What do you want to write?")
            time.sleep(2)  # Allow Notepad to open

            content = command()

            with open(file_path, "a") as file:
                file.write("\n" + content)
            
            speak("Content added successfully.")
        else:
            speak("Sorry, that file does not exist.")

    else:
        speak("I didn't understand. Please say 'new' or 'existing'.")


def final():
    # wishme()
    while(True):
        # query=input("Enter your command")
        query=command().lower()
        if ("open google" in query) or ("edge" in query):
            browsing(query)
        elif("close google" in query) or ("close instagram" in query) or ("close facebook" in query) or ("close whatsapp" in query) or ("close discord" in query):
            close_website("google")
        elif('facebook' in query) or ('discord' in query) or ('whatsapp' in query) or ('instagram' in query) or ('phub' in query)  or ('p hub' in query):
            social_media(query)
        elif ("volume up" in query) or ("increase volume" in query):
            pyautogui.press("volumeup") 
            speak("Volume increased")
        elif ("volume down" in query) or ("decrease volume" in query):
            pyautogui.press("volumedown") 
            speak("Volume decreased")
        elif ("volume mute" in query) or ("mute" in query):
            speak("Volume muted")
            pyautogui.press("volumemute")  
        elif("open calculator" in query) or ("open notepad" in query):
            openapp(query)
        elif("close calculator" in query) or ("close notepad" in query):
            closeapp(query)
        elif ("time" in query):
            now = datetime.datetime.now()
            current_time = now.strftime("%I:%M %p")  # Example: "02:45 PM"
            time.sleep(0.5)  # Add a short pause before speaking
            speak(f"It's {current_time}")
            # continue
        elif("condition" in query):
            condition()
        elif ("date" in query) or ("day" in query):
            now = datetime.datetime.now()
            current_date = now.strftime("%A, %B %d, %Y")  # Example: "Sunday, March 30, 2025"
            time.sleep(0.5)  # Add a short pause before speaking
            speak(f"Today is {current_date}")
            # continue
        elif "recognise the song" in query:
            time.sleep(1)
            asyncio.run(recognize_song())  # Use run() instead of get_event_loop()
        elif ("greet our sir" in query):
            speak("hi sir how are you")
        elif("what" in query) or ("who" in query) or ("how" in query) or ("hi" in query) or ("hello" in query) or ("thanks" in query) or ("joke" in query) or ("you" in query):
            padded_sequences = pad_sequences(tokenizer.texts_to_sequences([query]), maxlen=20, truncating='post')
            result = model.predict(padded_sequences)
            tag = label_encoder.inverse_transform([np.argmax(result)])

            for i in data['commands']:
                if i['tag'] == tag:
                    response=np.random.choice(i['responses'])
                    print(response)
                    time.sleep(0.3)
                    speak(response)

        elif ("system condition" in query) or ("constition of the system"in query):
                speak("checking the conditions")
                condition()
        elif "exit" in query:
            speak("thank you for listening ,we are open for questions now")
            speak_for_exit("change your GR please")
            sys.exit()

if __name__ == '__main__':
    final()