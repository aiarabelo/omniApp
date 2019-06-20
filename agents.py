import virtualenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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
        self.get("file:///C:/Users/aiarabelo/Desktop/Projects/omniApp/testpage.html")
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
            inputElementList = questionPair[key].find_elements_by_tag_name("input")
            if key not in userData.keys():
                continue
            else:
                inputElementList[0].send_keys(userData[key])
                

test = LeverAgent(False, r"C:\Users\aiarabelo\Desktop\Projects\omniApp\chromedriver.exe")

userData = {
        "Resume/CV" : "file:///C:/Users/aiarabelo/Desktop/Projects/OmniApp/resume.pdf",
        "Full name" : "Allison Arabelo",
        "Email" : "arabelo.aa@gmail.com",
        "Phone" : "628-241-9814",
        "Current company" : "Enishi.ai",
        "Twitter URL" : "",
        "LinkedIn URL" : "https://www.linkedin.com/in/allisonarabelo/",
        "GitHub URL" : "https://github.com/aiarabelo", 
        "Portfolio URL" : "http://www.allisonarabelo.com/",
        "Other website" : "",
        "At the time of applying, are you 18 years of age or older?" : "Yes",
        #TODO make this generalized for other countries "... to work in [country]"
        #TODO make the sponsorship questions more generalized
        "Are you legally authorized to work in the United States?" : "No",
        "Are you legally authorized to work in the country for which you are applying" : "No",
        "Will you now or in the future require sponsorship for employment visa status e g H 1B etc" : "Yes",
        "Will you now or in the future require sponsorship for employment visa status" : "Yes",
        "Do you currently, or in the future will you, require sponsorship to legally work in the United States?" : "Yes",
        "Language Skill s Check all that apply" : ["English (ENG)"],
        "Where are you applying from" : "United States [USA]",
        "How did you hear about this job?" : "Other",
        #"Which university are you currently attending or did you last attend Please select Other School Not Listed if your school is not listed" : "University of California - Berkeley",
        "Please tell us how you heard about this opportunity" : "Other",
        "What has been your favorite project or proudest accomplishment Why" : "TEST TEST TEST",
        "Gender" : "Female",
        "Race" : "Asian (Not Hispanic or Latino)",
        "Veteran status" : "I am not a veteran",
        "I certify the information and answers provided by me within this application are true and correct." : "Yes"
}

test.autoInputQuestion(test.getQuestionDict(), userData)


#driver.get("http://www.python.org")
#class: application-label