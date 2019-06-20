test = LeverAgent(False, r"C:\Users\aiarabelo\Desktop\Prnojects\omniApp\chromedriver.exe")
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
        self.get("file:///C:/Users/aiarabelo/Desktop/Projects/omniApp/testpage.html")
        questions = self.driver.find_elements_by_class_name("application-label")
        questionPair = {}
        for question in questions:
            print(elem.text.split("\n")[0])
            questionPair['question'] = 'x'
        questionPair.items()

test = LeverAgent(False, r"C:\Users\aiarabelo\Desktop\Prnojects\omniApp\chromedriver.exe")
test.getQuestionDict()