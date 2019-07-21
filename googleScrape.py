from googlesearch import search
import time
import re
import requests
import json
from jobPost import JobPost
from companiesdb import Company


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
        filteredURLs: a set of filtered URLs
        companies: a list of filtered URLs, no duplicates
        Purpose: Writes the resulting scraped company names onto a different file, of format baseURL.txt
        """
        i = 1
        companyURLs = []
        filteredURLs = set()

        for companyURL in search('site:' + baseURL, stop = 25000):
            print(companyURL)
            i+=1
            if i % 10 == 0:
                time.sleep(60)
            companyURLs.append(companyURL)

        for url in companyURLs:
            regex = r"(?:https?:\/\/(?:www\.)?" + baseURL + r"\/)([^/\n?\$]+)"
            r = re.search(regex, url)
            if r is not None:
                print("FILTERED! " + r.group(1))
                filteredURLs.add(r.group(1))
                try: 
                    Company().insertInfo(r.group(1), baseURL, r.group(0))
                except:
                    print("Error adding details to database for: " + url)
                    print(r.group(1) + " is a possible duplicate.")
                    pass
        
    ''' 
    TODO: This is currently hardcoded for lever only, fix that
    '''
    def getJobPosts(self, companyName):
        r = requests.get("https://api.lever.co/v0/postings/" + companyName)
        j = json.loads(r.text)
        return [JobPost(d) for d in j]
    
    # TODO: This filters for commitment and position only.
    #       For final product, filter for others
    def filterCompany(self, commitment, position, companyName, companyDetails):
        filteredCompany = list(filter(lambda x : commitment in x[0] and position in x[1], companyDetails[companyName]))
        return filteredCompany

if __name__ == "__main__":
    for atsURL in atsURLs:
        WebScraper().companyInfo(atsURL)