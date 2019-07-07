import os
from googleScrape import WebScraper
from agents import Agent, LeverAgent

if __name__ == "__main__":
    userData = {
      "Resume/CV" : "./resume.pdf",
      "Full name" : "Zachary Chao",
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
      "Disability status" : "No, I don't have a disability"
    }

    # Scrapes Google for companies on Lever if the .txt file of scraped URLs doesn't exist yet
    if not os.path.exists("./jobs.lever.co.txt"):
        WebScraper().companyInfo("jobs.lever.co")

    # Scrapes Google for companies on Greenhouse if the .txt file of scraped URLs doesn't exist yet
    if not os.path.exists("./boards.greenhouse.io.txt"):
        WebScraper().companyInfo("boards.greenhouse.io")
    
    # Extracts the company names from the ATS text files
    with open("jobs.lever.co.txt", "r") as f:
        leverCompanyNames = f.read().split("\n")

    with open("boards.greenhouse.io.txt", "r") as g:
        greenhouseCompanyNames = g.read().split("\n")
    
    # Lists details of the job posting: commitment, title, and applyUrl
    companyDetails = {}
    for companyName in leverCompanyNames:
        jobPostList = WebScraper().getJobPosts(companyName) # This is for Lever only
        companyDetails[companyName] = [[item.commitment, item.title, item.applyUrl] for item in jobPostList]
    
    # Filters out what we want for the job commitment and title
    jobPostList = list(filter(lambda x : "Intern" in x[0] and "Software Engineer" in x[1], companyDetails[companyName]))

    # Fill out the job applications' easy questions
    leverCrawler = LeverAgent(False, r".\chromedriver.exe")
    for item in jobPostList:
        leverCrawler.autoInputQuestion(leverCrawler.getQuestionDict(item[2]), userData)
