from selenium import webdriver
import pyttsx3 as p
import time
from selenium.webdriver.common.keys import Keys
from pynput.keyboard import Key, Controller

class ChromeHandler:
        def __init__(self):
            self.driver=webdriver.Chrome(executable_path='C:/Users/asus/.spyder-py3/chromedriver')
            

        
        def SearchWiki(self,query):
            self.driver.maximize_window()
            #self.driver.get("https://www.google.com")
            self.query=query
            self.driver.get(url="https://www.wikipedia.org/")
            search=self.driver.find_element_by_id('searchInput')
            search.click()
            search.send_keys(query)
                
            enter=self.driver.find_element_by_xpath('//*[@id="search-form"]/fieldset/button')
            enter.click()
            
            information=self.driver.find_element_by_xpath('//*[@id="mw-content-text"]/div/p[2]')
            #print(information)
            readable=information.text
            #print(readable)
            engine=p.init() 
            engine.setProperty('rate',170)
            voices = engine.getProperty('voices') 
            engine.setProperty('voice', voices[1].id)
            engine.say(readable)
            engine.runAndWait()
    
        def GoogSearch(self,query):
            self.driver.maximize_window()
            self.query=query
            self.driver.get(url="https://www.google.com/")
            search_box=self.driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input')
            search_box.click()
            search_box.send_keys(query)
            submit_bt=self.driver.find_element_by_xpath("//*[@id='tsf']/div[2]/div[1]/div[2]/div[2]/div[2]/center/input[1]")
            submit_bt.click()
            
        def playVideo(self,query):
            self.driver.maximize_window()
            self.driver.get(url="https://www.youtube.com/results?search_query="+query)
            video=self.driver.find_element_by_xpath('//*[@id="dismissable"]')
            video.click()
            
        def getWeather(self,location):
            try:
                self.driver.maximize_window()
                self.driver.get(url="https://www.accuweather.com/en/search-locations?query="+location)
              
                precise_loc=self.driver.find_element_by_xpath('//*[@class="search-results"]/a[1]')
                precise_loc.click()
                
                self.driver.implicitly_wait(5)
                temperature=self.driver.find_element_by_xpath('/html/body/div/div[5]/div[1]/div[1]/a[1]/div[1]/div[1]/div/div/div[2]')
                print(temperature)
                info=temperature.text
                print(info)
                #airquality=self.driver.find_element_by_xpath('/html/body/div/div[5]/div[1]/div[1]/a[1]/div[1]/div[2]/div[1]')
                
                #air=airquality.text
                #print(info,air)
                engine=p.init() 
                engine.setProperty('rate',170)
                voices = engine.getProperty('voices') 
                engine.setProperty('voice', voices[1].id)
                engine.say(info)
                #engine.say(air)
                engine.runAndWait()
            except:
                pass
            
            print(info)     
        def getLocation(self):
            self.driver.maximize_window()
            self.driver.get(url="https://mycurrentlocation.net/")
            time.sleep(3)
            longitude = self.driver.find_elements_by_xpath('//*[@id="longitude"]')#Replace with any XPath    
            longitude = [x.text for x in longitude]    
            longitude = str(longitude[0])    
            latitude = self.driver.find_elements_by_xpath('//*[@id="latitude"]')    
            latitude = [x.text for x in latitude]    
            latitude = str(latitude[0])    
            
            self.driver.get(url="https://www.google.com/maps")
            self.driver.implicitly_wait(5)
            
            search=self.driver.find_element_by_xpath('//*[@id="searchboxinput"]')
            print(latitude,longitude)
            key=latitude+','+longitude
            print(key)
            search.send_keys(key)
            button=self.driver.find_element_by_xpath('//*[@id="searchbox-searchbutton"]')
           
            button.click()      
        cnt=0     
        def navigate(self,path):
           self.driver.maximize_window()
           self.driver.execute_script("window.open();")
           self.cnt+=1
           print(self.cnt)    
           self.driver.switch_to.window(self.driver.window_handles[self.cnt])
           self.driver.get(path)
