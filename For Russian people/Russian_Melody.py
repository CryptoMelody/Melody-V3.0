#MELODY Current Version is 3.0 
#Warning: For this code use Python version 3.13 and lower, cause of the library "pygame"!!! 
import pygame
import time
import os
import webbrowser
import json
import pyaudio
import urllib.parse
from vosk import Model, KaldiRecognizer
from openai import OpenAI
import pyttsx3 
import argparse
import requests
import re
v = "1"
v_1 = "0"
esp_address = "192.168.8.20"
T = True
pygame.mixer.init()
#CHAT-GPT:
client = OpenAI (
    base_url = "https://api.sambanova.ai/v1", 
    api_key = "9b9c8b8f-3e5a-468c-8d46-7db3c82d1794" #use hugging face instead of OpenRouter (blocked site)
    )

#model = Model(r"D:\Voices\vosk-model-small-en-us-0.15")
#rec = KaldiRecognizer(model, 16000)
model_2  = Model(r"D:\Voices\vosk-model-small-ru-0.22")
rec = KaldiRecognizer(model_2, 16000)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()




def google_search(query):
    search_url = f"https://www.google.com/search?q={query}"
    search_url = search_url.replace(' ', '+')
    webbrowser.open(search_url)

def listen():
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if (rec.AcceptWaveform(data)) and (len(data) > 0):
            answer = json.loads(rec.Result())
            if answer['text']:
                yield answer['text']

def play_sound(file_path):
  
    try:
        
        if not os.path.exists(file_path):
            print(f"Audio file not found: {file_path}")
            return False
        
      
        try:
        
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            return True
        except pygame.error:
        
            try:
                sound = pygame.mixer.Sound(file_path)
                sound.play()
                time.sleep(sound.get_length() + 0.5)
                return True
            except:
                
                print(f"Using system player for: {file_path}")
                os.system(f'start "" "{file_path}"')
                time.sleep(2)  
                return True
                
    except Exception as e:
        print(f"Error playing sound {file_path}: {e}")
        return False

def process_command(command):
    #repaired 

    if 'открой' in command:
        site = None
        s = command.split("открой", 1)[1].strip()
        if "браузер" in s:
            site = "https://yandex.com"
        if "ютуб" in s:
            site = "https://youtube.com"
        if "почту" in s:
            site = "https://mail.ru"
        
        if site:
            play_sound(r"D:\Voices\33.wav")
            webbrowser.open(site)
        else:
            print(f"Unknown site")
            
    if "найди" in command :
        p = command.split("найди", 1)[1].strip()
        play_sound(r"D:\Voices\52.wav")
        google_search(p)
        
    if "запусти" in command:
        p = command.split("запусти", 1)[1].strip()
        if "браузер" in p:
            os.system(f"start browser.exe")
            play_sound(r"D:\Voices\16.wav")
        else:
            play_sound(r"D:\Voices\2.wav")
            print('Unknown programm')

    #CHAT-GPT:
    elif command.lower().startswith("джарвис"):
        p = command[7:].strip()

        completion = client.chat.completions.create (
            model = "Meta-Llama-3.3-70B-Instruct",
            messages = [
        {"role": "system", 
         "content": "Speak like a friend" 
         },                                 
        {"role": "user",
         "content": p
         },
      ],
            )
        #TTS-model
        engine = pyttsx3.init()
        voices = engine.getProperty("voices")
        engine.setProperty("voice", voices[0].id)  # CHECK THE CODE "For russian language" and change the index (find Irina) (for me it is "0" index)
        engine.say(completion.choices[0].message.content)
        engine.runAndWait()

def welcome(T):

    if T is True:
        play_sound(r"D:\Voices\35.wav")
        T = False
    return T

welcome(T)

for text in listen():
    print(f"Recognized: {text}") 
    
    #repaired 
    if "я сделал это" in text or "ура" in text or "я очень рад" in text:
        play_sound(r"D:\Voices\10.wav")
        
    if "спасибо" in text or "спасибо тебе" in text:
        play_sound(r"D:\Voices\54.wav")

    if "ты" in text and "тупой" in text:
        play_sound(r"D:\Voices\37.wav")

    if "статус" in text and "лампочки" in text:
        r = requests.get(f"http://{esp_address}/get").text
        if r == "1":
            play_sound(r"D:\Voices\33.wav")
            print("-ON-")
        else:
          play_sound(r"D:\Voices\33.wav")
          print("-OFF-")
    #connect the Melody's system with the smart house      
  
    if "включи" in text and "лампочку" in text:
        r = requests.post(f"http://{esp_address}/update", data=v)
        play_sound(r"D:\Voices\52.wav")
      
    if "выключи" in text and "лампочку" in text:
        r = requests.post(f'http://{esp_address}/update', data= v_1)
        play_sound(r"D:\Voices\52.wav")
       
        
    else:
      process_command(text)



