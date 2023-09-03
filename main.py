import pyttsx3
import datetime
import speech_recognition as sr
import smtplib
from info import senderemail, pwd, key, host, corona_host
from email.message import EmailMessage
import pyautogui
import webbrowser as wb
from time import sleep
import wikipedia
import pywhatkit
import requests
import clipboard
import AppOpener
import pyjokes
import time as tt
import string
import random
import psutil
import pyaudio

from tkinter import *

import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
from keras.models import load_model
model = load_model('chatbot_model.h5')
import json
import random





intents = json.loads(open('C:\\Users\\VICKY NJR\\PycharmProjects\\CARL\\intents.json').read())
words = pickle.load(open('C:\\Users\\VICKY NJR\\PycharmProjects\\CARL\\words.pkl','rb'))
classes = pickle.load(open('C:\\Users\\VICKY NJR\\PycharmProjects\\CARL\\classes.pkl','rb'))

print(intents["intents"][0])

def clean_up_sentence(sentence):
    # tokenize the pattern - splitting words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stemming every word - reducing to base form
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words


# return bag of words array: 0 or 1 for words that exist in sentence
def bag_of_words(sentence, words, show_details=True):
    # tokenizing patterns
    sentence_words = clean_up_sentence(sentence)
    # bag of words - vocabulary matrix
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,word in enumerate(words):
            if word == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % word)
    return(np.array(bag))

def predict_class(sentence):
    # filter below  threshold predictions
    
    p = bag_of_words(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sorting strength probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list


def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

def ask():
    ask = input("Ask me anything: ")
    predict = predict_class(ask)
    res = getResponse(predict, intents)
    print(res)


# while True:
# ask()
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("rate", 150)
engine.setProperty("voice", voices[0].id)


def speak(audio):
    engine.say(audio)
    # predict = predict_class(audio)
    # res = getResponse(predict, intents)
    # engine.say(res)
    engine.runAndWait()


def predict():
    query = takeCommandMic().lower()
    predict = predict_class(query)
    res = getResponse(predict, intents)
    engine.say(res)
    engine.runAndWait()


def welcome():
    speak("hello i am jarvis how can i help you")


def time():
    Time = datetime.datetime.now().strftime("%I:%M:%S")
    speak(f"the current time is {Time}")
    print(Time)


def date():
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    date = int(datetime.datetime.now().day)
    speak(f"the current date is {date} {month} {year}")
    print(date, month, year)


def takeCommandCMD():
    query = input("what can I do for you?\n")
    return query


def takeCommandMic():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, 2)
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        query = r.recognize_google(audio, language="en-IN")
        tokenized_query = nltk.word_tokenize(query)
        # predict = predict_class(query)
        # res = getResponse(predict, intents)
        print(tokenized_query)
        print(query)

    except Exception as e:
        print(e)
        speak("say that again...")
        return "None"
    return query


def sendEmail(receiver, subject, content):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(senderemail, pwd)
    email = EmailMessage()
    email["From"] = senderemail
    email["To"] = receiver
    email["Subject"] = subject
    email.set_content(content)
    server.send_message(email)
    server.close()


def sendwhatsappmsg(phone_no, message):
    Message = message
    wb.open("http://web.whatsapp.com/send?phone="+phone_no+"&text="+Message)
    sleep(10)
    pyautogui.press("enter")


def searchgoogle():
    speak("what should i search")
    search = takeCommandMic()
    wb.open("https://www.google.com/search?q="+search)


def text2speech():
    text = clipboard.paste()
    print(text)
    speak(text)


def covid():
    url = "https://covid-19-statistics.p.rapidapi.com/reports/total"

    querystring = {"date": "2023-01-05"}

    headers = {
        
        "X-RapidAPI-Key": key,
        "X-RapidAPI-Host": corona_host
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)


def screenshot():
    name_img = tt.time()
    name_img = f"C:\\Users\\VICKY NJR\\PycharmProjects\\CARL\\screenshot\\{name_img}.png"
    img = pyautogui.screenshot(name_img)
    img.show()


def passwordgen():
    s1 = string.ascii_uppercase
    s2 = string.ascii_lowercase
    s3 = string.digits
    s4 = string.punctuation

    passlen = 8

    s = []
    s.extend(list(s1))
    s.extend(list(s2))
    s.extend(list(s3))
    s.extend(list(s4))

    random.shuffle(s)
    new_pass = ("".join(s[0:passlen]))
    print(new_pass)
    speak(new_pass)


def flip():
    speak("flipping a coin")
    coin = ["heads", "tails"]
    toss = []
    toss.extend(coin)
    random.shuffle(toss)
    toss = ("".join(toss[0]))
    print(toss)
    speak("you got "+toss)


def roll():
    speak("rolling a die")
    die = ["1", "2", "3", "4", "5", "6"]
    rolling = []
    rolling.extend(die)
    random.shuffle(rolling)
    rolling = ("".join(rolling[0]))
    print(rolling)
    speak("you got "+rolling)


def cpu():
    usage = str(psutil.cpu_percent())
    speak("your cpu usage is "+usage)
    battery = psutil.sensors_battery()
    speak("your battery percentage is")
    speak(battery.percent)


if __name__ == "__main__":
    # wakeword = "jarvis"
    # if wakeword in takeCommandMic().lower():
        welcome() 
        while True:
            query = takeCommandMic().lower()
            print(query)
            if "talk" in query:
                speak("sure")
                predict()
            elif "time" in query:
                time()

            elif "date" in query:
                date()

            elif "email" in query:
                email_list = {
                    "karthi": "karthikk6702@gmail.com"
                }
                try:
                    speak("whom do you want to the mail")
                    name = takeCommandMic()
                    receiver = email_list[name]
                    speak("what is the subject of the mail")
                    subject = takeCommandMic()
                    speak("what should i say")
                    content = takeCommandMic()
                    sendEmail(receiver, subject, content)
                except Exception as e:
                    print(e)
                    speak("unable to send the mail")

            elif "message" in query:
                user_name = {
                    "karthi": "+91 8056208161"
                }
                try:
                    speak("whom do you want to the whatsapp message")
                    name = takeCommandMic()
                    phone_no = user_name[name]
                    speak("what is the message")
                    message = takeCommandMic()
                    sendwhatsappmsg(phone_no, message)
                    speak("message has been sent")
                except Exception as e:
                    print(e)
                    speak("unable to send the message")

            elif "wikipedia" in query:
                speak("searching on wikipedia")
                query = query.replace("wikipedia", "")
                result = wikipedia.summary(query, sentences=3)
                print(result)
                speak(result)

            elif "search" in query:
                searchgoogle()

            elif "youtube" in query:
                speak("what should i search in youtube")
                topic = takeCommandMic()
                pywhatkit.playonyt(topic)

            elif "weather" in query:
                speak("in which city do you want to know")
                city_name = takeCommandMic()
                # url = f"https://open-weather13.p.rapidapi.com/city/{city_name}"
                #
                # headers = {
                #     "X-RapidAPI-Key": key,
                #     "X-RapidAPI-Host": host
                # }
                #
                # response = requests.get(url, headers=headers)
                #
                # result = response.json()
                # print(result)
                url = "https://weatherapi-com.p.rapidapi.com/forecast.json"

                querystring = {"q": city_name, "days": "3"}

                headers = {
                    "X-RapidAPI-Key": key,
                    "X-RapidAPI-Host": host
                }

                response = requests.request("GET", url, headers=headers, params=querystring)

                print(response)
                # print(response.text)

            elif "news" in query:
                speak("which news do you want to know")
                news = takeCommandMic()
                #url = "https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey=f23f04e5315e4bbcbaa86033fabfc6e1"
                url = f"https://newsapi.org/v2/everything?q={news}&from=2023-01-03&to=2023-01-03&sortBy=popularity&apiKey=f23f04e5315e4bbcbaa86033fabfc6e1"
                response = requests.get(url)
                result = response.json()
                # print(result)
                speak(result["articles"][0]["title"])

            elif "read" in query:
                text2speech()

            elif "covid" in query:
                covid()

            elif "open" in query:
                query.replace("open", "")
                AppOpener.open(query, match_closest=True)

            elif "close" in query:
                query.replace("close", "")
                AppOpener.close(query, match_closest=True)

            elif "joke" in query:
                speak(pyjokes.get_joke())

            elif "screenshot" in query:
                screenshot()

            elif "remember" in query:
                speak("what should i remember")
                data = takeCommandMic()
                speak("you said me to remember that"+data)
                remember = open("data.txt", "w")
                remember.write(data)
                remember.close()

            elif "forgot something" in query:
                remember = open("data.txt", "r")
                speak("you told me to remember that"+remember.read())

            elif "generate password" in query:
                passwordgen()

            elif "flip" in query:
                flip()

            elif "roll" in query:
                roll()

            elif "CPU" in query:
                cpu()

            elif "offline" in query:
                quit()
