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

    """
    FUNCTION: Scrapes the given webpage for questions 
    questions and moreQuestions: element objects of the questions
    questionPair: a dictionary containing questions as they key, 
                and the corresponding WebElements as values
    userData: a dictionary containing the questions as the key, 
            and the answers as values
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
            print("@@@@ Question Label @@@@ ")
            print(questionLabel.text + "(" +str(len(questionLabel.text))+")")
            print("@@@@ outerHTML of each label @@@@ " + questionLabel.get_attribute("innerHTML"))

        # For Lever's "Additional Question" for cover letters/supplementary information
        additionalQuestion = self.driver.find_element_by_class_name("application-additional")
        additionalQuestionText = additionalQuestion.find_element_by_tag_name("textarea")
        questionPair[additionalQuestionText.get_attribute("placeholder")] = additionalQuestion

        return questionPair

    def get(self, url):
        self.driver.get(url)

class LeverAgent(Agent):
    def __init__(self, headless, chrome_executable_path):
        super().__init__(headless, chrome_executable_path)
    
    '''
    TODO: If checkForShortAnswers is True, abort this job post
    as we do not currently support that feature.
    '''
    """
    FUNCTION: Fills out the application page
    questionPair: a dictionary containing questions as they key, 
                and the corresponding WebElements as values
    userData: a dictionary containing the questions as the key, 
            and the answers as values

    #TODO: Stop if question was unanswered, if there are short answers; break if cover letter space

    """
    def autoInputQuestion(self, questionPair, userData):
        print("Filling out...")
        continueIndicator = 0
        for key in questionPair.keys():
            inputAnswer = questionPair[key].find_elements_by_tag_name("input")
            selectAnswer = questionPair[key].find_elements_by_tag_name("select")
            textareaAnswer = questionPair[key].find_elements_by_tag_name("textarea")
            if key not in userData.keys():
                continueIndicator += 1
            elif len(inputAnswer) == 1:  
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
            # elif len(textareaAnswer) == 0: 
            #     doNotSubmit = False
            elif len(textareaAnswer) == 1:
                continueIndicator += 1
            else:
                continueIndicator += 1
        print("There are "+ str(continueIndicator) +" unanswered questions.")
        if continueIndicator == 0:
            self.submitForm()
            #self.driver.close()             

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
   
    # TODO: Actually implement this. This does not check it simply returns True.
    """
    FUNCTION: Returns "True" if there are short answers 
    """
    def checkForShortAnswers(self):
        return True
    
    """
    FUNCTION: Submits the form
    inputAnswer: List of WebElements of choices that are checkboxes 
    userAnswer: A string, the answer(s) of the user to the question 
    
    """

    def submitForm(self):
        self.driver.find_element_by_tag_name("button").submit()
name = "Zachary Chao"
userData = {
      "Resume/CV" : "C:/Users/aiarabelo/Desktop/Projects/Github/omniApp/resume.pdf",
      "Full name" : "Zachary Chao",
      "Your name" : "Zachary Chao",
      "Email" : "zachchao@berkeley.edu",
      "Phone" : "760-889-1965",
      "Current company" : "CrossInstall",
      "Twitter URL" : "",
      "LinkedIn URL" : "https://www.linkedin.com/in/zacharychao/",
      "GitHub URL" : "https://www.github.com/zachchao", 
      "Portfolio URL" : "http://www.zacharychao.com/",
      "Other website" : "",
      "At the time of applying, are you 18 years of age or older?" : "Yes",
      "Are you legally authorized to work in the United States?" : "Yes",
      "Are you legally authorized to work in the country for which you are applying" : "Yes",
      "Are you currently authorized to work in the U.S.?" : "Yes",
      "Will you now or in the future require Rigetti Quantum Computing to commence (\"sponsor\") an immigration case in order to employ you?" : "No",
      "Will you now or in the future require sponsorship for employment visa status e g H 1B etc" : "No",
      "Will you now or in the future require sponsorship for employment visa status" : "No",
      "When are you seeking to begin a full-time position?" : "Immediately", 
      "Do you currently, or in the future will you, require sponsorship to legally work in the United States?" : "No",
      "Were you referred to Rigetti?" : ["No"], 
      "If so, by whom?" : "",
      "Language Skill s Check all that apply" : ["English (ENG)"],
      "Where are you applying from" : "United States [USA]",
      "How did you hear about this job?" : "LinkedIn",
      "Please tell us how you heard about this opportunity" : "Other",
      "Gender" : "Male",
      "Race" : "Asian (Not Hispanic or Latino)",
      "Veteran status" : "I am not a protected veteran",
      "I certify the information and answers provided by me within this application are true and correct." : "I Accept / I Agree",
      "Disability status" : "No, I don't have a disability",
      "Today’s date" : "07/09/19"
}

if __name__ == "__main__":
    
    leverCrawler = LeverAgent(False, "./chromedriver.exe")
    leverCrawler.autoInputQuestion(leverCrawler.getQuestionDict("file:///C:/Users/aiarabelo/Desktop/Projects/Github/omniApp/testpage3.html"), userData)