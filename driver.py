import os
from googleScrape import WebScraper

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
        greenhouseCompanyNames = g.read().split("\n")
    
    # Returns a dictionary of the job posting's commitment, title, and applyUrl
    companyDetails = {}
    for companyName in companyNames:
        jobPostList = WebScraper().getJobPosts(companyName) # This is for Lever only
        companyDetails[companyName] = [[item.commitment, item.title, item.applyUrl] for item in jobPostList]
        jobPostList = list(filter(lambda x : "Intern" in x[0] and "Software Engineer" in x[1], companyDetails[companyName]))
        filter(lambda x: if  , companyDetails[companyName])

    print([str(item) for item in WebScraper().getJobPosts(companyName)])