from googlesearch import search
import time
import re
import requests
import json
from jobPost import JobPost
from models import Company, CompanyJobs
from createEngine import createSession
from geomapping import convertToCoordinates


class WebScraper:
    def getCompanyInfo(self, baseURL):
        """
        FUNCTION: Scrapes Google for Company URLs and their names
        companyURL: each scraped item in the Google search
        companyURLs: an unfiltered list of company URLs; these may contain duplicate companies
        baseURL: the base URL of the ATS that will be scraped
        unfilteredURL: URL of company sites that will be scraped in Google
        r: filtered company URL; is of format <baseURL>/company
        filteredURLs: a set of filtered URLs
        companies: a list of filtered URLs, no duplicates
        Purpose: Writes the resulting scraped company names onto a different file, of format baseURL.txt
        """
        i = 1
        companyURLs = []
        companyNames = set()

        for companyURL in search("site:" + baseURL, stop=25000):
            print(companyURL)
            i += 1
            if i % 10 == 0:
                time.sleep(60)
            companyURLs.append(companyURL)

        session = createSession()
        for url in companyURLs:
            regex = r"(?:https?:\/\/(?:www\.)?" + baseURL + r"\/)([^/\n?\$]+)"
            r = re.search(regex, url)
            if r is not None:
                print("Adding to 'companies' list: " + r.group(1) + "...")
                companyNames.add(r.group(1))
                
        companyNames = list(companyNames)
        for companyName in companyNames:
            link = "https://" + baseURL + "/" + companyName
            try:
                Company(company_name=companyName, ats=baseURL, url=link).insert(session)
            except:
                print("Error adding details to database for: " + url)
                print(r.group(1) + " already exists in the table.")
                pass
        session.commit()
        session.close()


    """ 
    TODO: This is currently hardcoded for lever only, fix that
    """
    """
    FUNCTION: Gets the job posts for each company
    companyName: name of the company
    JobPost: a class in jobPost.py that retrieves job post attributes
    returns a list of webelements of job posts with relevant information
    """

    def listJobPosts(self, companyName):
        r = requests.get("https://api.lever.co/v0/postings/" + companyName)
        j = json.loads(r.text)
        return [JobPost(d) for d in j]

    """
    FUNCTION: Scrapes the job postings for each company and puts them in a database called job_listings
    companyName: name of the company
    """

    def scrapeJobPosts(self, session, companyName):
        jobPostList = self.listJobPosts(companyName)
        for item in jobPostList:
            CompanyJobs(company_name=companyName, commitment=item.commitment, department=item.department, location=convertToCoordinates(item.location), team=item.team, title=item.title, apply_url=item.applyUrl).insert(session)
            session.commit()
        print("Completed database input for job listings from " + companyName)

    """
    FUNCTION: Filters job postings for a company based on the desired commitment and position
    commitment: desired commitment (Intern, full-time, etc.)
    position: desired position (Software engineer, etc.)
    companyName: name of the company whose job postings will be filtered
    companyDetails: List of job postings for each companyName
    returns filteredCompany, a filtered list of job postings for a company
    """
    # TODO: This filters for commitment and position only.
    #       For final product, filter for others
    def filterCompany(self, session, commitment, title):
        filteredCompanies = CompanyJobs().filterJobListings(session, commitment=commitment, title=title)
        return filteredCompanies