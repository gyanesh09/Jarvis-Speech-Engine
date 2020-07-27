from selenium import webdriver
import pyttsx3 as p

class Wiki:
    
    def __init__(self):
        self.driver=webdriver.Chrome(executable_path='C:/Users/asus/.spyder-py3/chromedriver')
    
    def SearchWiki(self,query):
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
        

class Google:
    def __init__(self):        
        self.driver=webdriver.Chrome(executable_path='C:/Users/asus/.spyder-py3/chromedriver')
        
    def GoogSearch(self,query):
        self.query=query
        self.driver.get(url="https://www.google.com/")
        search_box=self.driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input')
        search_box.click()
        search_box.send_keys(query)
        submit_bt=self.driver.find_element_by_xpath("//*[@id='tsf']/div[2]/div[1]/div[2]/div[2]/div[2]/center/input[1]")
        submit_bt.click()
        
class YouTube:
    def __init__(self):
        self.driver=webdriver.Chrome(executable_path='C:/Users/asus/.spyder-py3/chromedriver')
        
    def playVideo(self,query):
        self.driver.get(url="https://www.youtube.com/results?search_query="+query)
        video=self.driver.find_element_by_xpath('//*[@id="dismissable"]')
        video.click()
        
        
class Weather:
    def __init__(self):
        self.driver=webdriver.Chrome(executable_path='C:/Users/asus/.spyder-py3/chromedriver')
        
    def getWeather(self,location):
        self.driver.get(url="https://www.accuweather.com/en/search-locations?query="+location)
        precise_loc=self.driver.find_element_by_xpath('//*[@class="search-results"]/a[1]')
        precise_loc.click()
        
        
        temperature=self.driver.find_element_by_xpath('//*[@class="template-root"]/div')
        print(temperature)
        info=temperature.text
        
        engine=p.init() 
        engine.setProperty('rate',170)
        voices = engine.getProperty('voices') 
        engine.setProperty('voice', voices[1].id)
        engine.say(info)
        engine.runAndWait()    
        
        print(info)
        
    
    

#div[1]/div[1]/a[1]/div[1]/div[1]
