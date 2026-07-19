import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')

for index, voice in enumerate(voices):
    print(f"Индекс: {index} | Имя: {voice.name} | Язык: {voice.languages}")
