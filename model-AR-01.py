"""
import speech_recognition as sr
from gtts import gTTS
import pygame
import os
import time
import pyttsx3

# the api funtion 
from openchat_api import get_ai_response

# initialize pygame mixture once
pygame.mixer.init() 

def speak(text):
    tts = gTTS(text=text, lang='en')
    filename = "temp.mp3"
    tts.save(filename)  # save the temp mp3 file before playing

    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.stop()  # it stops the audio after it gets played 
    pygame.mixer.music.unload()
    time.sleep(0.2)
    os.remove(filename)

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening.....")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        print("you said:", text)
        return text
    
    except sr.UnknownValueError:
        print("sorry i could not understand the audio.")
        return ""
    
    except sr.Request as e:
        print(f"could not request result; {e}")
        return ""
    
if __name__ == "__main__":
    speak("hello im AR zero1. how can i help you today?")
    while True:
        command = listen()
        if command.lower() == "exit":
            speak("goodbye!")
            break

        elif command:
            reply = get_ai_response(command) # uses the api function
            print("AR 01:", reply)
            speak(reply)
"""            



import speech_recognition as sr
import pyttsx3
import time
import socket

# the api funtion 
from openchat_api import get_ai_response

engine = pyttsx3.init()
engine.setProperty('rate', 180)  # Speed of speech

def speak(text):
    engine.say(text)
    engine.runAndWait()

def check_internet(hosts=["8.8.8.8", "1.1.1.1", "google.com"]):
    for host in hosts:
        try:
            socket.create_connection((host, 80), timeout=3)
            return True
        except (OSError, socket.timeout):
            continue
    return False    



def listen():
    r = sr.Recognizer()
    with sr.Microphone(device_index=0) as source:  # ensures the current mic avaiable on your machine
        print("listening.....")
        r.adjust_for_ambient_noise(source, duration=1) # reduce noice adjustment time
        r.dynamic_energy_threshold = True

        try:
            audio = r.listen(source, timeout=8, phrase_time_limit=8)
        except sr.WaitTimeoutError:
            print("No speech detected. try again.")
            speak("I didn't hear anything. Please repeat,")
            return ""

        try:
            text = r.recognize_google(audio, language='en-US')
            print("You said:", text)
            return text.strip()
        except sr.UnknownValueError:
            print("Could not understand audio.")
            speak("Sorry, I didn't catch that. Could you repeat?")
            return ""
        except sr.RequestError as e:
            print(f"Speech recognition error: {e}")
            speak("There was an error with the speech service.")
            return ""
        
        
    
if __name__ == "__main__":
    offline_alerted = False
    speak("hello im AR zero1. how can i help you today?")
    
    while True:
        if not check_internet():
            if not offline_alerted:
                speak("you are not connected to the internet. Please check your connection.")
                print("waiting for internet connection....")
                offline_alerted = True               
                time.sleep(5)  # wait for 5 sec before checking it again
            continue
        else:
            offline_alerted = False
            
                
        command = listen()
        if command.lower() == "exit":
            speak("goodbye!")
            break

        elif command:
            reply = get_ai_response(command) # uses the api function
            print("AR 01:", reply)
            speak(reply)

         