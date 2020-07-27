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
import datetime

# setting pyttsx3 for speak functionality
engine=p.init('sapi5') 
engine.setProperty('rate',170)
voices = engine.getProperty('voices') 
engine.setProperty('voice', voices[1].id)


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
        r.adjust_for_ambient_noise(source, duration=0.5)
      
        audio=r.listen(source)
        said=""
        try:
            print("Recognizing...")
            said=r.recognize_google(audio)
        except:
            print("sorry can not understand")
            
    return said

def chat():
    print("Start talking with CoroVac (say quit to stop)!")
    x = datetime.datetime.now()
    x=x.hour

    if x<12 and x>=0:
        greet="GoodMorning Mate How can I help You"
        
    elif x>=12 and x<18:
        greet="GoodAfternoon Mate How can i help you"
    else:
        greet ="GoodEvening Mate How acn I help You"
        
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
            if "quit" in text:
                speak("Goodbye see you again!")
                break
            
            elif 'open google maps' in text:
                 flag=0
                 cnt=0
                 webbrowser.open("www.google.com/maps")
                 
            elif 'open google' in text:
                flag=0
                cnt=0
                webbrowser.open("www.google.com")
            elif 'open calculator' in text:
                flag=0
                cnt=0
                subprocess.Popen('C:\\Windows\\System32\\calc.exe')
            elif 'open visual studio code' in text:
                flag=0
                cnt=0
                os.startfile("C:/Users/asus/AppData/Local/Programs/Microsoft VS Code/Code.exe")
            elif 'search wikipedia' in text:
                flag=0
                cnt=0
                print("from inside",text)
                list1=list(text.split())
                print(list1)
                query=''
                for i in list1:
                    if i !='search' and i!='wikipedia':
                        query+=i
                        query+=" "
                print(query) 
                obj=Wiki()
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
                obj=Google()
                obj.GoogSearch(query)
            elif 'open camera' in text:
                flag=0
                cnt=0
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
                    obj=Weather()
                    obj.getWeather(query)
                except:
                    pass
            elif 'play music' in text:
                flag=0
                cnt=0
                list1=list(text.split())
                query=''
                for i in list1:
                    if i !='play' and i!='music':
                        query+=i
                        query+=" "
                obj=YouTube()
                obj.playVideo(query)
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
                    try:
                        cnt+=1
                    except:
                        cnt=1
                    if cnt>=3:
                        speak("No response Mate Goodbyeee See You later")
                        break
                    speak("Sorry,I dont know that")
chat()