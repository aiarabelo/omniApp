from googlesearch import search
import time
import re
import requests
import json
from jobPost import JobPost
from models import Company, CompanyJobs
from createEngine import createSession


atsURLs = ["boards.greenhouse.io", "jobs.lever.co"]

class WebScraper:
    def companyInfo(self, baseURL):
        """
        FUNCTION: Scrapes Google for Company URLs
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
        filteredURLs = set()

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
                print("FILTERED! " + r.group(1))
                filteredURLs.add(r.group(1))
                try:
                    company = Company(company_name=r.group(1), ats=baseURL, url=r.group(0)).insert(session)
                except:
                    print("Error adding details to database for: " + url)
                    print(r.group(1) + " is a possible duplicate.")
                    pass
            
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

    def scrapeJobPosts(self, companyName):
        jobPostList = self.listJobPosts(companyName)
        for item in jobPostList:
            CompanyJobs(company_name=companyName, commitment=item.commitment, department=item.department, location=item.location, team=item.team, title=item.title, apply_url=item.applyUrl).insert(session)
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
    def filterCompany(self, commitment, position, companyName, companyDetails):
        filteredCompany = list(
            filter(
                lambda x: commitment in x[0] and position in x[1],
                companyDetails[companyName],
            )
        )
        return filteredCompany


if __name__ == "__main__":
    for atsURL in atsURLs:
        WebScraper().companyInfo(atsURL)
