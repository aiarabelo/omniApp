import os
from googleScrape import WebScraper
from agents import Agent, LeverAgent
import time
from companiesdb import Company
import psycopg2
import pdb

if __name__ == "__main__":
    # Scrapes Google for companies on Lever if the .txt file of scraped URLs doesn't exist yet
    if not os.path.exists("./jobs.lever.co.txt"):
        WebScraper().companyInfo("jobs.lever.co")

    # Scrapes Google for companies on Greenhouse if the .txt file of scraped URLs doesn't exist yet
    if not os.path.exists("./boards.greenhouse.io.txt"):
        WebScraper().companyInfo("boards.greenhouse.io")
    
    # Extracts the company names from the ATS text files (This is hardcoded; remove this when generalized to Greenhouse too)
    with open("jobs.lever.co.txt", "r") as f:
        print("Extracting company names from Lever...")
        leverCompanyNames = f.read().split("\n")
        leverCompanyNames = leverCompanyNames[:-1]

        print(type(leverCompanyNames))
        print("Extraction done!")

    with open("boards.greenhouse.io.txt", "r") as g:
        print("Extracting company names from Greenhouse...")
        greenhouseCompanyNames = g.read().split("\n")   
        greenhouseCompanyNames = greenhouseCompanyNames[:-1]     
        print("Extraction done!")

    # companyDetails: dictionary, with the company name as key and its value being a list of job postings for that company
    # Lists details of the job posting: commitment, title, and applyUrl
    companyDetails = {}
    filteredCompanyDetails = []
    # TODO: Generalize this for all ATS

    for companyName in leverCompanyNames:
        print("Extracting job postings from " + companyName +"...")
        jobPostList = WebScraper().getJobPosts(companyName) # This is for Lever only
        try:
            companyDetails[companyName] = [[item.commitment, item.title, item.applyUrl, companyName] for item in jobPostList]
        except: 
            print("Error for extracting details from " + companyName)
            pass
        print(companyDetails[companyName])
        print("Extraction complete for "+ companyName+"!")
        print("Filtering...")
        filteredCompanyDetails.extend(list(filter(lambda x : "Intern" in x[0] and "Software Engineer" in x[1], companyDetails[companyName])))
    
    # Filters out what we want for the job commitment and title from the dictionary "companyDetails"
    print("Filtered! Here is what's left:")
    print(filteredCompanyDetails)
    print("@@@@@ END OF FILTERED COMPANY DETAILS @@@@@")

    # Load user data
    userFile = "userdata.json"
    with open(userFile, "r") as f:
        userData = json.loads(f.read())
    # Fill out the job applications' easy questions
    for item in filteredCompanyDetails:
        leverCrawler = LeverAgent(False, "./chromedriver.exe")
        print("Applying to " + item[3] + "...")
        try:
            leverCrawler.autoInputQuestion(leverCrawler.getQuestionDict(item[2]), userData)
        except:
            print("Error in application for "+ item[3]+": "+item[1] + " (" + item[0] + ").")
            pass
        time.sleep(60)
