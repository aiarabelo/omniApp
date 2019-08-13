import os
from googleScrape import WebScraper
from agents import Agent, LeverAgent
import time
from models import Company, CompanyJobs
from createEngine import createSession
import psycopg2
import json
import pdb


atsURLs = ["boards.greenhouse.io", "jobs.lever.co"]

if __name__ == "__main__":
    # companyDetails: dictionary, with the company name as key and its value being a list of job postings for that company
    # Lists details of the job posting: commitment, title, and applyUrl
    companyDetails = {}
    filteredCompanyDetails = []

    session = createSession()
        
    """
    FUNCTION: Creates "companies" and "job_listings" tables 
    Uncomment this to scrape company names. 
    """
    # for atsURL in atsURLs:
    #     WebScraper().getCompanyInfo(atsURL)

    
    # Hardcoded: Getting company names off the ATS
    leverCompanyNames = Company.getCompanyNames(session, "jobs.lever.co")

    # Uncomment this to not hardcode:
    # commitment = input("Desired commitment: ")
    # position = input("Desired position: ")
    # location = input("Desired location: ")
    # Hardcoded:
    commitment = "Intern"
    title = "Software"
    location = "San Francisco"
        
    """
    FUNCTION: Scrapes company job listings  
    Uncomment this to scrape job listings per company. 
    """
    # TODO: Generalize this for all ATS
    # i=0 # For testing
    for companyName in leverCompanyNames:
        print("Extracting job postings from " + companyName + "...")
        jobPostList = WebScraper().listJobPosts(companyName)  # This is for Lever only
        try:
            companyDetails[companyName] = [[item.commitment, item.title, item.applyUrl, companyName] for item in jobPostList]
            WebScraper().scrapeJobPosts(session, companyName)
        except:
            print("Error for extracting details from " + companyName)

        print(companyDetails[companyName])
        print("Extraction complete for " + companyName + "!")
        # i += 1
        # if i % 10 == 0:
        #     break
    
    try: 
        filteredCompanyDetails.extend(WebScraper().filterCompany(session, commitment, title))
    except: 
        print("Duplicate entry. Skipping...")
    # Filters out what we want for the job commitment and title from the dictionary "companyDetails"
    print("Filtered! Here is what's left:")
    print(filteredCompanyDetails)
    print("@@@@@ END OF FILTERED COMPANY DETAILS @@@@@")

    # Load user data
    # TODO: Use a database instead
    with open("userdata.json", "r") as f:
        userData = json.loads(f.read())

    # Fill out the job applications' easy questions
    # TODO: Clear textbox before sending keys, items should correspond to database entries
    # for item in filteredCompanyDetails:
    #     leverCrawler = LeverAgent(False, "./chromedriver.exe")
    #     print("Applying to " + item + "...")
    #     try:
    #         leverCrawler.autoInputQuestion(leverCrawler.getQuestionDict(item), userData)
    #     except:
    #         print(
    #             "Error in application for "
    #             + session.query(CompanyJobs.company_name)[0]
    #             + ": "
    #             + session.query(CompanyJobs.title)[0]
    #             + " ("
    #             + session.query(CompanyJobs.commitment)[0]
    #             + ")."
    #         )
    #         pass
    #     time.sleep(60)
    session.close()
    
