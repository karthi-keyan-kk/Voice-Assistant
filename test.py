import speech_recognition as sr
import pyttsx3


r = sr.Recognizer()
with sr.Microphone() as source:
    print("Listening...")
    r.adjust_for_ambient_noise(source, 2)
    r.pause_threshold = 1
    audio = r.listen(source)
    # print(audio)
    query = r.recognize_google(audio, language="en-IN")
print(query)

engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)

engine.say(query)