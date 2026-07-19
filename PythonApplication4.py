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
v = "1"
v_1 = "0"
esp_address = "164.568.4.15"
T = True 
pygame.mixer.init()
#CHAT-GPT:
client = OpenAI (
    base_url = "https://api.sambanova.ai/v1", 
    api_key = "df4654626-9sdf4-789f54-954f-hf798456" #use sambanova instead of OpenRouter (blocked site for me)
    )

model = Model(r"D:\Voices\vosk-model-small-en-us-0.15")
rec = KaldiRecognizer(model, 16000)
#model_2  = Model(r"D:\Voices\vosk-model-small-ru-0.22")
#rec = KaldiRecognizer(model_2, 16000)

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

    if 'find' in command:
        site = None
        s = command.split("find", 1)[1].strip()
        if "browser" in s:
            site = "https://yandex.com"
        if "youtube" in s or "you tube" in s:
            site = "https://youtube.com"
        if "mail" in s:
            site = "https://mail.ru"
        
        if site:
            play_sound(r"D:\Voices\33.wav")
            webbrowser.open(site)
        else:
            print(f"Unknown site")
            
    if "search for" in command :
        p = command.split("search for", 1)[1].strip()
        play_sound(r"D:\Voices\52.wav")
        google_search(p)
        
    if "open" in command:
        p = command.split("open", 1)[1].strip()
        if "browser" in p:
            os.system(f"start browser.exe")
            play_sound(r"D:\Voices\16.wav")
        else:
            play_sound(r"D:\Voices\2.wav")
            print('Unknown programm')

    #CHAT-GPT:
    elif command.lower().startswith("melody"):
        p = command[7:].strip()
        completion = client.chat.completions.create (
            model = "DeepSeek-V3.1",
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
        engine.setProperty("voice", voices[1].id)
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
    if "i made it" in text or "i did it" in text or "hurray" in text:
        play_sound(r"D:\Voices\10.wav")
        
    if "thanks" in text or "thank you" in text or "спасибо" in text:
        play_sound(r"D:\Voices\54.wav")

    if "you" in text and "asshole" in text:
        play_sound(r"D:\Voices\37.wav")

    if "status" in text and "of" in text and "light" in text:
        r = requests.get(f"http://{esp_address}/get").text
        if r == "1":
            play_sound(r"D:\Voices\33.wav")
            print("-ON-")
        else:
          play_sound(r"D:\Voices\33.wav")
          print("-OFF-")
    #connect the Melody's system with the smart house      
  
    if "turn" in text and "lights" in text and "on" in text:
        r = requests.post(f"http://{esp_address}/update", data=v)
        play_sound(r"D:\Voices\52.wav")
      
    if "turn" in text and "lights" in text and "off" in text:
        r = requests.post(f'http://{esp_address}/update', data= v_1)
        play_sound(r"D:\Voices\52.wav")
       
        
    else:
      process_command(text)


