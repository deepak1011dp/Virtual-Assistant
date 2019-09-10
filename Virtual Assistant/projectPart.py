import speech_recognition as sr
from pynput.keyboard import Key, Controller
from bs4 import BeautifulSoup as soup
import os
import sys
import re
import pyttsx3
import webbrowser
import smtplib 
import subprocess
import vlc
import urllib
import urllib3
import requests, json
import time as t
import wikipedia
import random
import pandas as pd
from time import strftime
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

global word
#Convert Text To Speech
def ghostResponse(audio):
    engine = pyttsx3.init()
    engine.setProperty('voice', 'english+f5')
    engine.setProperty('rate', 150)
    engine.say(audio)
    engine.runAndWait()
print('Ready ')
ghostResponse('I am Ready ')
word = '' #whatever we say
global flag
def myCommand(): #Recognizer
    r = sr.Recognizer()
    r.energy_threshold = 2100
    global word
    with sr.Microphone() as source:
        print('Say Something...')
        try:
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source)
        except:
            print('Timed Out, Speak Again ! ')
            audio = r.listen(source)
    try:
        command = r.recognize_google(audio, language = 'en-IN') #.lower
        print('You said: ' + command + '\n')
        #loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        print('Could not Recognize Sir')
        command = myCommand()
    return command

def email():
    ghostResponse('Who is the recipient?')
    recipient = myCommand()
    if '@' in recipient:
        ghostResponse('What should I say to him?')
        content = myCommand()
        mail = smtplib.SMTP('smtp.gmail.com', 587)
        mail.ehlo()
        mail.starttls()
        mail.login('itsmesender@gmail.com','sender123')
        mail.sendmail('itsmesender@gmail.com', recipient, content)
        mail.close()
        ghostResponse('Email has been sent successfuly. You can check your inbox.')
    else:
        ghostResponse('I don\'t know what you mean!,try again')

def launch(word):
    app = word.split(' ')
    app = app[1]
    f2=pd.read_csv('/home/deepak/PROJECT/Apath.csv')
    app_list=f2['App'].tolist()
    if app in app_list:
        ind=app_list.index(app)
        subprocess.Popen(f2['path'][ind])

    elif 'youtube' in app:
        youtube()
    elif 'gesture' in word:
            d='giving you gesture control sir...use green colour for mouse control'
            print(d)
            speak(d)
            gesture_control()
    elif 'keyboard' in word:
        keyboard()
    else:
        ghostResponse('Application Not Found !')
        print('Application Not Found')
        word=myCommand()
        if 'enter path' in word: 
            user_input=input('enter path ')
            new_app=pd.DataFrame({'App':[app],'path':[user_input]})
            f2=pd.concat([f2,new_app],ignore_index=True)
            print(f2)
            ghostResponse('do you want me to save it in database for future reference')
            if 'yes' in word:
                f2.to_csv('/home/deepak/PROJECT/Apath.csv',index=False)
            else:
                pass
            subprocess.Popen(user_input)
        else:
            pass
    

def brightness(word):
    word1 = word.split(' ')
    if 'increase' in word1:
        os.system('amixer -D pulse sset Master 5%+')
    if 'decrease' in word1:
        os.system('amixer -D pulse sset Master 5%-')

def news():
    raw=urllib.request.urlopen("http://newsapi.org/v1/articles?source=the-times-of-india&By=top&apikey=efba2e263d6c41bea0ec49e96754ae99")
    myjson=raw.read()
    a=json.loads(myjson.decode())
    for i in range(0,5):
        print("Headlines number"+str(i+1)+" is")
        result = a['articles'][i]['title']
        print(result)
        ghostResponse(result)
def youtube():
    driver = webdriver.Chrome('/home/deepak/PROJECT/chromedriver')
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    ghostResponse('whats your mood sir? Which song do you want to listen?')
    song=myCommand()
    driver.get("https://www.youtube.com/results?search_query=" + str(song))
    ids=driver.find_elements_by_xpath('//*[@href]')
    for ii in ids:
        k=ii.get_attribute('href')
        if(k[24:29]=='watch'):
            z=k
            break
        else:
            pass
    driver.get(z)
    driver.get(z) 

def weather():
    ghostResponse("Tell me your city sir")
    city_name=myCommand()
    print("city you said is",city_name)
    #city_name=input("enter city name to confirm")
    api_key = "cca979ed5fb2c8d3a9c99594191482f9"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name 
    json_data=requests.get(complete_url).json()
    try:
        temp=json_data['main']
        temp=str(int(int(temp['temp'])-273.15))
        temp1=json_data['weather'][0]['description']
        d =" Current Temperature in "+city_name+" is "+temp+" degree celsius with "+temp1
        print("Ghost : ",d)
        ghostResponse(d)
    except KeyError:
        print("Key invalid or city not found")

#use green coloured band for gesture control
#for clicking  just move the cursor to required position and move the coloured
#tape a bit forword
#to close the gesture control move the cursor to "BOTTOM RIGHT" corner
#and it will automatically close.
def gesture_control():
    area_list=[]
    v=cv2.VideoCapture(0)
    ges=1
    while(ges==1):
        ret,i=v.read()
        j=cv2.cvtColor(i,cv2.COLOR_BGR2GRAY)
        k=i[:,:,1]
        A=[]
        g=cv2.subtract(k,j)
        g=cv2.multiply(g,5)
        r,g=cv2.threshold(g,50,255,0)
        cnt,_=cv2.findContours(g,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        #print(len(cnt))
        #print(cnt)
        for i in range(0,len(cnt)):
                area=cv2.contourArea(cnt[i])
                A.append(area)
                
        if(len(cnt)>0):
            amax=max(A)
            #print(amax)
            if(len(area_list)==10):
                del area_list[0]
                if(area_list[8]-area_list[0]>1000):
                    ms.click(Button.left)
                    ms.release(Button.left)          
            if(len(area_list)<10):
                area_list.append(amax)
            ind=A.index(amax)
            M=cv2.moments(cnt[ind])
            #print(M)
            if(M['m00']>0.0):
                cx=int(M['m10']/M['m00'])
                cy=int(M['m01']/M['m00'])
                ms=Controller()
                ms.position=(3*cx,3*cy)
                if ms.position[0] in range(1270,1365) and ms.position[1] in range(675,687):
                    ges=0
            else:
                pass
        else:
            pass
        print(area_list)
        #time.sleep(5)
        
        l=cv2.waitKey(1)
        if(l==ord(' ')):
            cv2.destroyAllWindows()
            break
    v.release()

#open notepad and start typing by voice command

def keyboard():
    word = myCommand()
    print(word)
    k = Controller()
    if word == 'stoptyping':
        quit()
    elif word == 'fullstop':
        k.press('.')
        k.release('.')
    elif word == 'save':
        k.press(Key.ctrl)
        k.press('s')
        k.release('s')
        k.release(Key.ctrl)
    elif word == 'enter':
        k.press(Key.enter)
        k.release(Key.enter)
    elif word == 'space':
        k.press(Key.space)
        k.release(Key.space)
    elif word =='backspace':
        k.press(Key.backspace)
        k.release(Key.backspace)
        
    else:
        k.type(word)
#ghostResponse('Start Typing')
def conversation():
    flag = 0
    while(flag!=1):
        word=''
        print('Please say something')
        ghostResponse("Please say something")
        word = myCommand()
        if "hello" in  word or "hi ghost" in word or "hey ghost" in word or "ghost" in word:
            d = "Hello Deepak"
            print("Ghost : ", d)
            ghostResponse(d)
        elif 'launch' in word or 'open' in word:
            launch(word)
        elif 'email' in word:
            email()
        elif 'brightness' in word:
            brightness()
        elif 'news' in word:
            news()
        elif 'maximize window' in word:
            k = Controller()
            k.press(Key.alt)
            k.press(Key.f10)
            k.release(Key.f10)
            k.release(Key.alt)
        elif 'close window' in word:
            k = Controller()
            k.press(Key.alt)
            k.press(Key.f4)
            k.release(Key.f4)
            k.release(Key.alt)
        elif 'time' in  word:
            tttt=time.ctime()
            d = str(tttt[11:19])
            print("Ghost : ", d)
            ghostResponse(d)
        elif "date" in  word:
            tttt=time.ctime()
            d=tttt[4:11]+tttt[20:24]
            print("Ghost : ",d)
            ghostResponse(d)
        elif "day" in  word:
            tttt=time.ctime()
            day=tttt[0:3]
            di={'Mon':'Monday','Tue':'Tuesday','Wed':'Wednesday','Thu':'Thursday','Fri':'Friday','Sat':'Saturday','Sun':'Sunday'}
            d=di[day]
            print("Ghost : ",d)
        elif "doing" in  word or "doing here" in  word:
            d = "I am here to help you Sir"
            print("Ghost : ",d)
            ghostResponse(d)
        elif "how are you" in  word:
            d = "I am fine Sir."
            print("Ghost : ",d)
            ghostResponse(d)
        elif 'your name' in word or 'who are you' in word or'about yourself' in word:
            d = ['I am Ghost','I am your Virtual Assistant']
            d = d[random.randint(0,len(d)-1)]
            ghostResponse(d)

        elif "wikipedia" in word:
            txt_to_speech("what you want to search on wikipedia")
            se = myCommand()
            d=wikipedia.summary(se, sentences=2)
            print("Ghost :" , d)
            ghostResponse(d)
        
        elif "weather" in  word or "temperature" in  word:
            weather()
        elif "search from google" in word or "google for me" in word:
            ghostResponse("what you want to search")
            print("what to search")
            word2 = myCommand()
            for d in search(word2, tld="co.in", num=10, stop=10, pause=2):
                print(d)
                ghostResponse(d)
                
        elif "thank you" in  word or "thanks" in  word:
            d = "You're welcome Sir. I am just doing my job"
            print("Ghost : ",d)
            ghostResponse(d)    
            
        elif 'bye' in word or 'good bye' in word:
            flag = 0
        
        else:
            d = ['I am not trained for this','I do not understand','sorry, I dont know']
            d = d[random.randint(0,len(d)-1)]
            ghostResponse(d)

 
conversation()
              
        
