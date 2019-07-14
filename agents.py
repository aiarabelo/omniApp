import virtualenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
import json

class Agent:
    def __init__(self, headless, chrome_executable_path):
        self.headless = headless
        self.chrome_executable_path = chrome_executable_path
        options = Options()
        options.set_headless(headless=self.headless)
        self.driver = webdriver.Chrome(options=options, 
            executable_path=self.chrome_executable_path)

    """
    FUNCTION: Scrapes the given webpage for questions 
    questions: list of webelement objects for questions 
    question and additionalQuestion: webelement object corresponding to a question
    questionPair: a dictionary containing questions as they key, 
                and the corresponding WebElements as values
    questionLabel and additionalQuestionLabel: A question in the application (string)
    Returns questionPair, a dictionary containing questions and its corresponding webelement
    """
   
    def getQuestionDict(self, applyURL):
        self.get(applyURL)
        questionPair = {}
        questions = self.driver.find_elements_by_class_name("application-question")

        for question in questions:
            questionLabel = question.find_element_by_class_name("application-label") 
            if len(questionLabel.text) == 0: 
                questionPair[questionLabel.get_attribute("innerHTML")] = question
            else: 
                questionPair[questionLabel.text.split("\n")[0]] = question

        # For Lever's "Additional Question" for cover letters/supplementary information
        additionalQuestion = self.driver.find_element_by_class_name("application-additional")
        additionalQuestionLabel = additionalQuestion.find_element_by_tag_name("textarea")
        questionPair[additionalQuestionLabel.get_attribute("placeholder")] = additionalQuestion

        return questionPair

    def get(self, url):
        self.driver.get(url)

class LeverAgent(Agent):
    def __init__(self, headless, chrome_executable_path):
        super().__init__(headless, chrome_executable_path)
    
    """
    FUNCTION: Fills out the application page
    questionPair: a dictionary containing questions as the key, 
                and the corresponding WebElements as values
    userData: a dictionary containing the questions as the key, 
            and the answers as values

    """
    def autoInputQuestion(self, questionPair, userData):
        print("Filling out application form...")
        continueIndicator = 0
        for key in questionPair.keys():
            inputAnswer = questionPair[key].find_elements_by_tag_name("input")
            selectAnswer = questionPair[key].find_elements_by_tag_name("select")
            textareaAnswer = questionPair[key].find_elements_by_tag_name("textarea")

            if key not in userData.keys():
                self.answerAdditional(key, userData, userFile)

            self.pageInteract(key, inputAnswer, selectAnswer, textareaAnswer, userData, continueIndicator)
        
        print("There are " + str(continueIndicator) + " unanswered question(s).")
        # UNCOMMENT THIS TO ACTUALLY
        # if continueIndicator == 0:
        #     self.submitForm()
        #     self.driver.close()             

    #TODO: Alert if there are referral questions, or make a system for it 

    """
    FUNCTION: Prompts user to answer any questions that 
              haven't been answered and adds it to the json file
    question: question label as scraped from getQuestionDict, 
              this is the key in questionPair
    userData: dictionary of user data corresponding to questions
    userFile: filename containing the dictionary of userData

    """
    def answerAdditional(self, question, userData, userFile):
        additionalAnswer = input(question + ": ")
        userData[question] = additionalAnswer
        with open(userFile, "w+") as f:
            f.write(json.dumps(userData))
    
    """
    FUNCTION: Interacts with the page (answering questions) for autoInputQuestion
    inputAnswer: List of WebElements of choices of type radio
    selectAnswer: List of WebElements of choices of type selectAnswer
    textareaAnswer: List of WebElements of choices of type textareaAnswer
    question: question label as scraped from getQuestionDict, 
              this is the key in questionPair
    userData: dictionary of user data corresponding to questions
    userFile: filename containing the dictionary of userData
    
    """

    def pageInteract(self, question, inputAnswer, selectAnswer, textareaAnswer, userData, continueIndicator):
        if len(inputAnswer) == 1:  
            inputAnswer[0].send_keys(userData[question])
        elif len(inputAnswer) > 1:  
            inputType = inputAnswer[0].get_attribute("type")
            if inputType == "radio":
                self.radioInput(inputAnswer, userData[question])
            elif inputType == "checkbox": 
                self.checkboxInput(inputAnswer, userData[question])             
        elif len(selectAnswer) != 0: 
            select_element = Select(selectAnswer[0])
            select_element.select_by_visible_text(userData[question])
        elif len(textareaAnswer) == 1:
            textareaAnswer[0].send_keys(userData[question])
            continueIndicator += 1

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
    FUNCTION: Submits the form
    """
    def submitForm(self):
        self.driver.find_element_by_tag_name("button").submit()



if __name__ == "__main__":
    userFile = "userdata.json"
    with open(userFile, "r") as f:
        userData = json.loads(f.read())
    leverCrawler = LeverAgent(False, "./chromedriver.exe")
    leverCrawler.autoInputQuestion(leverCrawler.getQuestionDict("file:///C:/Users/aiarabelo/Desktop/Projects/Github/omniApp/testpage3.html"), userData)

