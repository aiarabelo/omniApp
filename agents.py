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

    '''
    Dictionary from question label to web element
    '''

    def getQuestionDict():
        raise NotImplementedError

class LeverAgent(Agent):
    def __init__(self, headless, chrome_executable_path):
        self.headless = headless
        self.chrome_executable_path = chrome_executable_path
        super().__init__()

    def get(self, url):
        self.driver.get(url)

    def getQuestionDict(self):
        #self.get("file:///C:/Users/aiarabelo/Desktop/Projects/omniApp/testpage.html")
        self.get("file:///C:/Users/aiarabelo/Desktop/Projects/omniApp/testpage2.html")
        questions = self.driver.find_elements_by_class_name("application-question")
        questionPair = {}
        for question in questions:
            questionLabel = question.find_element_by_class_name("application-label")
            questionPair[questionLabel.text.split("\n")[0]] = question
        return questionPair


    def autoInputQuestion(self, questionPair, userData):
        userDataSet = set(userData.keys())
        questionPairSet = set(questionPair.keys())

        for key in questionPair.keys():
            inputAnswer = questionPair[key].find_elements_by_tag_name("input")
            selectAnswer = questionPair[key].find_elements_by_tag_name("select")
            textareaAnswer = questionPair[key].find_elements_by_tag_name("textarea")
            
            print(key)
            print(len(inputAnswer)) 
            print(len(selectAnswer)) 
            print(len(textareaAnswer))

            if key not in userData.keys():
                continue
            elif len(inputAnswer) > 1:  
                inputType = inputAnswer[0].get_attribute("type")
                if inputType == "radio":
                    self.radioInput(inputAnswer, userData[key])
                elif inputType == "checkbox": 
                    continue 
                inputAnswer[0].send_keys(userData[key])
            elif len(inputAnswer) == 1:  
                inputAnswer[0].send_keys(userData[key])
            
            elif len(textareaAnswer) == 1:  
                textareaAnswer[0].send_keys(userData[key])
            elif len(selectAnswer) != 0: 
                select_element = Select(selectAnswer[0])
                select_element.select_by_visible_text(userData[key])
            else: 
                continue
                print("You have more things to do")     

    def radioInput(self, inputAnswer, userAnswer):
        choiceList = []
        for element in inputAnswer:
            choice = element.get_attribute("value")
            choiceList.append(choice)
            if userAnswer == choice:
                index = choiceList.index(choice)
                print(inputAnswer[index])
                print(choice)
                print(inputAnswer)
                print(userAnswer)
                print(index)
                print(choiceList)
                self.driver.execute_script("arguments[0].click();", inputAnswer[index])

    def checkboxInput(self): 
        pass

test = LeverAgent(False, r"C:\Users\aiarabelo\Desktop\Projects\omniApp\chromedriver.exe")
date = "06/21/2019"
userData = {
            "Resume/CV" : "C:/Users/aiarabelo/Desktop/Projects/OmniApp/resume.pdf",
            "Full name" : "Allison Arabelo",
            "Email" : "arabelo.aa@gmail.com",
            "Phone" : "628-241-9814",
            "Current company" : "Enishi.ai",
            "Twitter URL" : "",
            "LinkedIn URL" : "https://www.linkedin.com/in/allisonarabelo/",
            "GitHub URL" : "https://www.github.com/aiarabelo", 
            "Portfolio URL" : "http://www.allisonarabelo.com/",
            "Other website" : "",
            "At the time of applying, are you 18 years of age or older?" : "Yes",
            #TODO make this generalized for other countries "... to work in [country]"
            #TODO make the sponsorship questions more generalized
            "Are you legally authorized to work in the United States?" : "No",
            "Are you legally authorized to work in the country for which you are applying" : "No",
            "Are you currently authorized to work in the U.S.?" : "No",
            "Will you now or in the future require Rigetti Quantum Computing to commence (\"sponsor\") an immigration case in order to employ you?" : "Yes",
            "Will you now or in the future require sponsorship for employment visa status e g H 1B etc" : "Yes",
            "Will you now or in the future require sponsorship for employment visa status" : "Yes",
            "When are you seeking to begin a full-time position?" : "Immediately", 
            "Do you currently, or in the future will you, require sponsorship to legally work in the United States?" : "Yes",
            "Were you referred to Rigetti?" : "Yes", 
            "If so, by whom?" : "Daniel Setiawan",
            "Language Skill s Check all that apply" : ["English (ENG)"],
            "Where are you applying from" : "United States [USA]",
            "How did you hear about this job?" : "None of the above/Other",
            #"Which university are you currently attending or did you last attend Please select Other School Not Listed if your school is not listed" : "University of California - Berkeley",
            "Please tell us how you heard about this opportunity" : "Other",
            "What has been your favorite project or proudest accomplishment Why" : "TEST TEST TEST",
            "Gender" : "Female",
            "Race" : "Asian (Not Hispanic or Latino)",
            "Veteran status" : "I am not a protected veteran",
            "I certify the information and answers provided by me within this application are true and correct." : "I Accept / I Agree",
            "Disability status" : "No, I don't have a disability",
            "Your name" : "Allison Arabelo",
            "Today's date" : date,
}

test.autoInputQuestion(test.getQuestionDict(), userData)


#driver.get("http://www.python.org")
#class: application-label