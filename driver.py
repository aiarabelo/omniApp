import os
from googleScrape import WebScraper
from agents import Agent, LeverAgent
import time

# from companiesdb import Company, CompanyJobs
from models import Company
from createEngine import createSession
import psycopg2
import json
import pdb


if __name__ == "__main__":
    # companyDetails: dictionary, with the company name as key and its value being a list of job postings for that company
    # Lists details of the job posting: commitment, title, and applyUrl
    companyDetails = {}
    filteredCompanyDetails = []

    # Hardcoded: Getting company names off the ATS
    session = createSession()
    leverCompanyNames = Company.getCompanyNames(session, "jobs.lever.co")

    # Uncomment this to not hardcode:
    # commitment = input("Desired commitment: ")
    # position = input("Desired position: ")
    # Hardcoded:
    commitment = "Intern"
    position = "Software Engineer"

    # TODO: Generalize this for all ATS
    for companyName in leverCompanyNames:
        print("Extracting job postings from " + companyName + "...")
        jobPostList = WebScraper().listJobPosts(companyName)  # This is for Lever only
        try:
            companyDetails[companyName] = [
                [item.commitment, item.title, item.applyUrl, companyName]
                for item in jobPostList
            ]
            WebScraper().scrapeJobPosts(companyName)
        except:
            print("Error for extracting details from " + companyName)
            pass
        print(companyDetails[companyName])
        print("Extraction complete for " + companyName + "!")
        filteredCompanyDetails.extend(
            WebScraper().filterCompany(
                commitment, position, companyName, companyDetails
            )
        )

    # Filters out what we want for the job commitment and title from the dictionary "companyDetails"
    print("Filtered! Here is what's left:")
    print(filteredCompanyDetails)
    print("@@@@@ END OF FILTERED COMPANY DETAILS @@@@@")

    # Load user data
    # TODO: Use a database instead
    with open("userdata.json", "r") as f:
        userData = json.loads(f.read())

    # Fill out the job applications' easy questions
    # TODO: Clear textbox before sending keys
    for item in filteredCompanyDetails:
        leverCrawler = LeverAgent(False, "./chromedriver.exe")
        print("Applying to " + item[3] + "...")
        try:
            leverCrawler.autoInputQuestion(
                leverCrawler.getQuestionDict(item[2]), userData
            )
        except:
            print(
                "Error in application for "
                + item[3]
                + ": "
                + item[1]
                + " ("
                + item[0]
                + ")."
            )
            pass
        time.sleep(60)

    session.close()
