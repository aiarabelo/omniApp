from googlesearch import search
import time
import re
import requests
import json
from jobPost import JobPost

atsURLs = ['boards.greenhouse.io', 'jobs.lever.co']

class WebScraper:
    def companyInfo(self, baseURL):
        """
        FUNCTION: Scrapes Google for Company URLs
        companyURL: each scraped item in the Google search
        companyURLs: an unfiltered list of company URLs; these may contain duplicate companies
        baseURL: the base URL of the ATS that will be scraped
        unfilteredURL: URL of company sites that will be scraped in Google
        r: filtered company URL; is of format <baseURL>/company
        filteredURLs: a list of filtered URLs
        nameAndURL: dictionary containing the company URLs, with truncated company names as keys
        Purpose: Writes the resulting scraped websites onto a different file, of format baseURL.txt
        """
        i = 1
        companyURLs = []
        filteredURLs = []
        nameAndURL = {}
        with open(baseURL + ".txt", "w+") as companies:
            for companyURL in search('site:' + baseURL, stop = 25000):
                print(companyURL)
                i+=1
                if i % 10 == 0:
                    time.sleep(60)
                companyURLs.append(companyURL)
            for url in companyURLs:
                if baseURL == "boards.greenhouse.io":
                    r = re.search(r"(?:https:\/\/boards\.greenhouse\.io\/)([^/]+\/?$)", url)
                elif baseURL == "jobs.lever.co":
                    r = re.search(r"(?:https:\/\/jobs\.lever\.co\/)([^/]+\/?$)", url)
                if r is not None:
                    print("FILTERED! " + r.group(0))
                    if r not in filteredURLs:
                        filteredURLs.append(r.group(0))
                        companies.write(r.group(1)+"\n")
        #                 nameAndURL[r.group(1)] = r.group(0)          
        # return nameAndURL
    def getJobPosts(self, companyName):
        r = requests.get("https://api.lever.co/v0/postings/" + companyName)
        j = json.loads(r.text)
        return [JobPost(d) for d in j]

    def getJobList(self, company):
        print("Crawling: ")


if __name__ == "__main__":
    print(WebScraper().getJobPosts("bird"))