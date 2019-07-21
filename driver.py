import os
from googleScrape import WebScraper
from agents import Agent, LeverAgent
import time
from companiesdb import Company
import psycopg2
import json
import pdb


if __name__ == "__main__":
    # companyDetails: dictionary, with the company name as key and its value being a list of job postings for that company
    # Lists details of the job posting: commitment, title, and applyUrl
    companyDetails = {}
    filteredCompanyDetails = []

    # Hardcoded: Getting company names off the ATS
    leverCompanyNames = Company().getCompanyNames("jobs.lever.co")
    
    commitment = input("Desired commitment: ")
    position = input("Desired position: ") 
    # Hardcoded: 
    # commitment = Intern
    # position = Software Engineer

    # TODO: Generalize this for all ATS
    for companyName in leverCompanyNames:
        print("Extracting job postings from " + companyName + "...")
        jobPostList = WebScraper().getJobPosts(companyName) # This is for Lever only
        try:
            companyDetails[companyName] = [[item.commitment, item.title, item.applyUrl, companyName] for item in jobPostList]
        except: 
            print("Error for extracting details from " + companyName)
            pass
        print(companyDetails[companyName])
        print("Extraction complete for " + companyName + "!")
        filteredCompanyDetails.extend(WebScraper().filterCompany(commitment, position, companyName, companyDetails))
    
    # Filters out what we want for the job commitment and title from the dictionary "companyDetails"
    print("Filtered! Here is what's left:")
    print(filteredCompanyDetails)
    print("@@@@@ END OF FILTERED COMPANY DETAILS @@@@@")

    # Load user data
    # TODO: Use a database instead
    userFile = "userdata.json"
    with open(userFile, "r") as f:
        userData = json.loads(f.read())

    # Fill out the job applications' easy questions
    # TODO: Clear textbox before sending keys
    for item in filteredCompanyDetails:
        leverCrawler = LeverAgent(False, "./chromedriver.exe")
        print("Applying to " + item[3] + "...")
        try:
            leverCrawler.autoInputQuestion(leverCrawler.getQuestionDict(item[2]), userData)
        except:
            print("Error in application for " + item[3] + ": " + item[1] + " (" + item[0] + ").")
            pass
        time.sleep(60)
