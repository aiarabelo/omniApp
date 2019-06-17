import virtualenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

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
        d = {}
        questions = self.driver.find_elements_by_class_name('application-question')
        for question in questions:
            questionNameLabel = question.find_elements_by_class_name("application-label")
            if questionNameLabel != []:
                questionName = questionNameLabel[0].text
                # TO DO : Make this better - cuts out a lot of stuff
                questionName = " ".join(re.findall(r"\w+", questionName))
                d[questionName] = question
        return d
test = LeverAgent(False, r"C:\Users\aiarabelo\Desktop\Projects\omniApp\chromedriver.exe")
test.getQuestionDict()