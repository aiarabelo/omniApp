import virtualenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time

class Agent:
    def __init__(self, headless, chrome_executable_path):
        self.headless = headless
        self.chrome_executable_path = chrome_executable_path
        options = Options()
        options.set_headless(headless=self.headless)
        self.driver = webdriver.Chrome(options=options, 
            executable_path=self.chrome_executable_path)

    def getQuestionDict(self, applyURL):
        self.get(applyURL)
        questions = self.driver.find_elements_by_class_name("application-question")
        # disabilityQuestions = self.driver.find_elements_by_id("disabilitySignatureSection")
        # for disabilityQuestion in disabilityQuestions:
        #     additionalDisabilityQuestion = disabilityQuestion.find_elements_by_class_name("application-question")
        #     print(additionalDisabilityQuestion)
        #     questions.extend(additionalDisabilityQuestion)
        #     for x in additionalDisabilityQuestion:
        #         print("ADDITIONAL" + x.get_attribute("outerHTML"))
        questionPair = {}
        for question in questions:
            questionLabel = question.find_element_by_class_name("application-label") 
            if len(questionLabel.text) == 0: 
                questionPair[questionLabel.get_attribute("innerHTML")] = question
            else: 
                questionPair[questionLabel.text.split("\n")[0]] = question
            # print("@@@@ Question Label @@@@ ")
            # print(questionLabel.text + "(" +str(len(questionLabel.text))+")")
            # print("@@@@ outerHTML of each label @@@@ " + questionLabel.get_attribute("innerHTML"))
            
        print(questions)
        print("111111111111")
        # print(disabilityQuestions)
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ QUESTIONPAIR @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print(questionPair)
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ QUESTIONPAIR @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        #driver.find_element_by_xpath("//")
        #print(disabilityQuestion.get_attribute("outerHTML"))   
        # driver.find_element_by_xpath("//disabilitySignatureSection[div/@class='application-label']")

    def get(self, url):
        self.driver.get(url)

class LeverAgent(Agent):
    def __init__(self, headless, chrome_executable_path):
        super().__init__(headless, chrome_executable_path)
    
if __name__ == "__main__":
    leverCrawler = LeverAgent(False, "./chromedriver.exe")
    leverCrawler.getQuestionDict("file:///C:/Users/aiarabelo/Desktop/Projects/Github/omniApp/testpage2.html")
    