import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
import numpy
import tflearn
import tensorflow
import random
import json
import pickle
import speech_recognition as sr 
from gtts import gTTS 
import playsound  
import os 
import datetime
import pyttsx3 as p
import webbrowser
import subprocess
from WikiSearch import *
from chromehandler import *
import datetime
import time
import ctypes
# setting pyttsx3 for speak functionality
engine=p.init('sapi5') 
engine.setProperty('rate',180)
voices = engine.getProperty('voices') 
engine.setProperty('voice', voices[0].id)
SPI_SETDESKWALLPAPER = 20 

with open("intents.json") as file:
    data = json.load(file)

try:
    model.load("model.tfl")
    with open("data.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)
        
except:                         #training
    words = []
    labels = [] 
    docs_x = []
    docs_y = []

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])

        if intent["tag"] not in labels:
            labels.append(intent["tag"])

    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))

    labels = sorted(labels)

    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []

        wrds = [stemmer.stem(w.lower()) for w in doc]

        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)


    training = numpy.array(training)
    output = numpy.array(output)

    with open("data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)
    
    tensorflow.reset_default_graph()
        
    net = tflearn.input_data(shape=[None, len(training[0])])
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
    net = tflearn.regression(net)
        
    model = tflearn.DNN(net)
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("model.tfl")
    
    
def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
            
    return numpy.array(bag)
'''def speak(text):
    tts=gTTS(text=text,lang="en")
    date_string = datetime.datetime.now().strftime("%d%m%Y%H%M%S")
    filename="hello"+date_string+".mp3"
    tts.save(filename)
    playsound.playsound(filename)'''

def speak(text):
       engine.say(text) 
       engine.runAndWait()
    
def getAudio():    
    r=sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.2)
      
        audio=r.listen(source)
        said=""
        try:
            print("Recognizing...")
            said=r.recognize_google(audio)
        except:
            print("sorry can not understand")
            
    return said

def chat():
    print("Start talking with Thor (say quit to stop)!")
    x = datetime.datetime.now()
    x=x.hour

    if x<12 and x>=0:
        greet="Jarvis reporting..GoodMorning Sir! How can I help You"
    
    elif x>=12 and x<18:
        greet="Jarvis reporting.. GoodAfternoon Sir!How can i help you"
    else:
        greet ="Jarvis reporting.. GoodEvening Sir! How can I help You"
        
    speak(greet)
    print("User Guide:")
    print()
    print(":: Try search wikipedia {{search_key}}")
    print(":: Try play music {{music_name}}")
    print(":: Try Tell weather of {{city_name}}")
    print(":: Open any system apps with CoroVac!!")
    print(":: Try search Google {{search_key}}")
    print(":: Try open Google Maps")
    while True:     
            text=getAudio()
            print()
            print("You : ",text)
            text=text.lower()
            
            if "quit" in text or 'goodbye jarvis' in text or 'go to sleep jarvis' in text  or 'goodbye' in text:
                speak("Ok Sir!!Goodbye! see you again!")
                os.system("taskkill /f /im Rainmeter.exe")
                ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, "C:\\Users\\asus\\Desktop\\156841.jpg" , 3)
                break
            
            elif 'great' in text or 'nice' in text  or 'excellent' in text:
                speak("Thankyou  Sir!!... It's My pleasure")
            
            elif  'jarvis pls silent' in text or 'be silent' in text:
                speak("OK Sir!! As YOu wish")
                
                break
            elif 'describe yourself' in text:
                response="My name is Thor powered by 2.4giga hertz decacore processor with huge memory of 10 TEra BYtes iinbuilt system UFS2.0 version 3.........My Boss Is Gyanesh he has made my heart....Thanks for his gretafullness"
                speak(response)
                
            elif 'open google maps' in text:
                 speak("opening Google maps Sir")
                 flag=0
                 cnt=0
                 webbrowser.open("www.google.com/maps")
                 
            elif 'tell my location' in text or 'my location' in text or'current location' in text:
                speak("Locating Sir")
                try:
                    obj.getLocation()
                except:
                    obj=ChromeHandler() 
                    obj.getLocation()
                #obj=Location()
                #obj.getLocation()
                
            elif 'close google chrome' in text or 'close chrome' in text:
                speak("Ok Sir")
                os.system("taskkill /f /im chrome.exe")
       
            elif 'in mood of doing coding jarvis' in text or 'mood of doing coding' in text or 'mood of coding' in text or 'in mood of coding' in text or 'mood off coding' in text:
                speak("Sir shall I open codechef or codeforces")
                temp=getAudio().lower()
                print(temp)
                if 'codechef' in temp:
                    speak("Sure Sir")
                    webbrowser.open("https://www.codechef.com")
                else:
                    speak("Sure Sir")
                    webbrowser.open("https://codeforces.com")
                    
            elif 'navigate to' in text:
                list1=list(text.split())
                print(list1)
                query=''
                for i in list1:
                    if i !='navigate' and i!='to':
                        query+=i
                        query+=" "
                print(query) 
                query=query.strip()
                navpath="https://www."+query+".com"
                print(navpath)
                try:
                    obj.navigate(navpath)
                except:
                    obj=ChromeHandler() 
                    obj.navigate(navpath)
                
            elif 'do i have any facebook messages' in text or 'facebook messages' in text:
                speak("Opening facebook Sir")
                webbrowser.open("https://www.facebook.com")
                
            elif 'open google' in text:
                flag=0
                cnt=0
                speak("Opening Google Sir")
                webbrowser.open("www.google.com")
            elif 'open calculator' in text:
                flag=0
                cnt=0
                subprocess.Popen('C:\\Windows\\System32\\calc.exe')
           
            elif 'open visual studio code' in text:
                flag=0
                cnt=0
                speak("OK Sir! Code Hard")
                os.startfile("C:/Users/asus/AppData/Local/Programs/Microsoft VS Code/Code.exe")
               
            elif 'search wikipedia' in text:
                flag=0
                cnt=0
                
                list1=list(text.split())
                print(list1)
                query=''
                for i in list1:
                    if i !='search' and i!='wikipedia':
                        query+=i
                        query+=" "
                print(query) 
                speak("Searching Wikipedia")
                try:
                    obj.SearchWiki(query)
                except:
                    obj=ChromeHandler()       
                    obj.SearchWiki(query)
                
            elif 'search google' in text:
                flag=0
                cnt=0
                list1=list(text.split())
                query=''
                for i in list1:
                    if i !='search' and i!='google':
                        query+=i
                        query+=""
                speak("Searching Google")  
                try:
                   obj.GoogSearch(query)
                except:
                   obj=ChromeHandler()
                   obj.GoogSearch(query)
                    
                #obj=Google()
                #obj.GoogSearch(query)
                
            elif 'open camera' in text:
                flag=0
                cnt=0
                speak("Done MAte")
                subprocess.run('start microsoft.windows.camera:', shell=True)
                
            elif 'weather' in  text:
                flag=0
                cnt=0
                list1=list(text.split())
                query=''
                
                for i in list1:
                    if i !='tell' and i!='weather' and i!='of' and i!='me':
                        query+=i
                        query+=" "
                try:
                    speak("2 seconds Sir")
                    obj.getWeather(query)
                except:
                    obj=ChromeHandler()      
                    obj.getWeather(query)
             
            elif 'play music' in text:
                flag=0
                cnt=0
                list1=list(text.split())
                query=''
                for i in list1:
                    if i !='play' and i!='music':
                        query+=i
                        query+=" "
                        
                speak("playing music Sir")  
                try:
                    obj.playVideo(query)
                except:
                    obj=ChromeHandler()  
                    obj.playVideo(query)
                #obj=YouTube()
                #obj.playVideo(query)
                
            elif text=='':
                pass
            else:       
                results = model.predict([bag_of_words(text, words)])[0]
                results_index = numpy.argmax(results)
                tag = labels[results_index]
        
                if results[results_index]>0.7: 
                    flag=0
                    cnt=0
                    for tg in data["intents"]:
                        if tg['tag'] == tag:
                            responses = tg['responses']
            
                    speak(random.choice(responses))
                else:
                    speak("Sorry,I dont know that!May be later my knowledge could enhance")

r=sr.Recognizer()
while(True):
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.2)
        audio=r.listen(source)
        said=""
        try:
            print("Recognizing...")
            said=r.recognize_google(audio)
            print(said)
        except:
            print("sorry can not understand")
            
        if "jarvis wake up" in said.lower() or 'wake up' in said.lower() or "wakeup" in said.lower() or 'jarvis' in said.lower():    
            engine.say("Yes Sir! Starting Engine, Loading resources...Establishing Connection.!")  
            
            ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, "C:\\Users\\asus\\Desktop\\download.jfif" , 3)
            
            os.startfile("C:/Program Files/Rainmeter/Rainmeter.exe")
             
            chat()
            break 
'''elif text=="":
                    try:
                        cnt+=1
                    except:
                        cnt=1
                    if cnt>=8:
                        speak("No response Mate Goodbyeee.... See You later")
                        break'''        