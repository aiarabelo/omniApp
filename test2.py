from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#import pdb 

driver = webdriver.Chrome()
driver.get("file:///C:/Users/aiarabelo/Desktop/Projects/omniApp/testpage.html")
count = 0
for elem in driver.find_elements_by_class_name("application-label"):
	print(elem.text.split("\n")[0])
#pdb.set_trace()
driver.close()