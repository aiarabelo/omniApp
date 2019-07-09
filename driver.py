import os
from googleScrape import WebScraper
from agents import Agent, LeverAgent

if __name__ == "__main__":
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
        greenhouseCompanyNames = g.read().splito("\n")
    
    # Lists details of the job posting: commitment, title, and applyUrl
    companyDetails = {}
    for companyName in companyNames:
        jobPostList = WebScraper().getJobPosts(companyName) # This is for Lever only
        companyDetails[companyName] = [[item.commitment, item.title, item.applyUrl] for item in jobPostList]
    
    # Filters out what we want for the job commitment and title
    jobPostList = list(filter(lambda x : "Intern" in x[0] and "Software Engineer" in x[1], companyDetails[companyName]))

    # Fill out the job applications' easy questions
    leverCrawler = LeverAgent(False, "./chromedriver.exe")
    for item in jobPostList:
        leverCrawler.autoInputQuestion(leverCrawler.getQuestionDict(item[2]), userData)
