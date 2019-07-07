import virtualenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import pdb


class Agent:
    def __init__(self):
        options = Options()
        options.set_headless(headless=self.headless)
        self.driver = webdriver.Chrome(options=options, 
            executable_path=self.chrome_executable_path)

    def getQuestionDict(self, applyURL):
        """
        FUNCTION: Scrapes the given webpage for questions 
        questionPair: a dictionary containing questions as they key, 
                    and the corresponding WebElements as values
        userData: a dictionary containing the questions as the key, 
                and the answers as values
        Returns questionPair, a dictionary containing questions and its corresponding webelement
        """
        self.get(applyURL)
        questions = self.driver.find_elements_by_class_name("application-question")
        questionPair = {}
        for question in questions:
            questionLabel = question.find_element_by_class_name("application-label")
            questionPair[questionLabel.text.split("\n")[0]] = question
        return questionPair
        
class LeverAgent(Agent):
    def __init__(self, headless, chrome_executable_path):
        self.headless = headless
        self.chrome_executable_path = chrome_executable_path
        super().__init__()

    def get(self, url):
        self.driver.get(url)
    
    def autoInputQuestion(self, questionPair, userData):
        """
        FUNCTION: Fills out the application page
        questionPair: a dictionary containing questions as they key, 
                    and the corresponding WebElements as values
        userData: a dictionary containing the questions as the key, 
                and the answers as values
        
        """
        for key in questionPair.keys():
            inputAnswer = questionPair[key].find_elements_by_tag_name("input")
            selectAnswer = questionPair[key].find_elements_by_tag_name("select")
            textareaAnswer = questionPair[key].find_elements_by_tag_name("textarea")
            if key not in userData.keys():
                pass
            if len(inputAnswer) == 1:  
                inputAnswer[0].send_keys(userData[key])
            elif len(inputAnswer) > 1:  
                inputType = inputAnswer[0].get_attribute("type")
                if inputType == "radio":
                    self.radioInput(inputAnswer, userData[key])
                elif inputType == "checkbox": 
                    self.checkboxInput(inputAnswer, userData[key])             
            elif len(selectAnswer) != 0: 
                select_element = Select(selectAnswer[0])
                select_element.select_by_visible_text(userData[key])
            elif len(textareaAnswer) == 0: 
                return False
            elif len(textareaAnswer) == 1:
                self.checkForShortAnswers()

    #TODO: Alert if there are referral questions, or make a system for it 

    """
    FUNCTION: Fills out a radio input; used in the function "autoInputQuestion"
    inputAnswer: List of WebElements of choices of type radio
    userAnswer: A string, the answer of the user to the question 
    
    """
    def radioInput(self, inputAnswer, userAnswer):
        choices = [choice.get_attribute("value") for choice in inputAnswer]
        index = choices.index(userAnswer)
        self.driver.execute_script("arguments[0].click();", inputAnswer[index])
    
    """
    FUNCTION: Fills out a checkbox input; used in the function "autoInputQuestion"
    inputAnswer: List of WebElements of choices that are checkboxes 
    userAnswer: A string, the answer(s) of the user to the question 
    
    """
    def checkboxInput(self, inputAnswer, userAnswers): 
        for userAnswer in userAnswers:
            choices = [choice.get_attribute("value") for choice in inputAnswer]
            index = choices.index(userAnswer)
            self.driver.execute_script("arguments[0].click();", inputAnswer[index])
   
    """
    FUNCTION: Returns "True" if there are short answers 
    """
    def checkForShortAnswers(self):
        return True