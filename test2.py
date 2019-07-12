import virtualenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time

class Agent:
    def __init__(headless, chrome_executable_path):
        headless = headless
        chrome_executable_path = chrome_executable_path
        options = Options()
        options.set_headless(headless=headless)
        driver = webdriver.Chrome(options=options, 
            executable_path=chrome_executable_path)

    def getQuestionDict(applyURL):
        get(applyURL)
       
        questions = driver.find_elements_by_id("disabilitySignatureSection")
        #for question in questions:
        #subQuestions = questions.find_elements_by_class_name("application-label")
        #print(question)
        print(questions)
        #print(subQuestions)

    def get( url):
        driver.get(url)


if __name__ == "__main__":
    Agent(False, "./chromedriver.exe").getQuestionDict("file:///C:/Users/aiarabelo/Desktop/Projects/Github/omniApp/testpage2.html")