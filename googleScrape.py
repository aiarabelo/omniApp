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
        nameAndURL = {} # TODO: This is unused and I think you shouldn't have it. If you agree, remove it
        with open(baseURL + ".txt", "w+") as companies:
            '''
            TODO: This block does not use the file and should be outside of the 'with' block
            We try to make the time that we use a file as short as possible incase
            another file wants to access the same file so what exists in the with block
            should be only what is neccessary
            '''
            for companyURL in search('site:' + baseURL, stop = 25000):
                print(companyURL)
                i+=1
                if i % 10 == 0:
                    time.sleep(60)
                companyURLs.append(companyURL)
            for url in companyURLs:
                '''
                TODO: You can make this dynamic by constructing the regex by inserting the base url
                eg, regex = "(?:https:\/\/" + baseURL + r"\/)([^/]+\/?$)"
                '''
                if baseURL == "boards.greenhouse.io":
                    r = re.search(r"(?:https:\/\/boards\.greenhouse\.io\/)([^/]+\/?$)", url)
                elif baseURL == "jobs.lever.co":
                    r = re.search(r"(?:https:\/\/jobs\.lever\.co\/)([^/]+\/?$)", url)
                if r is not None:
                    print("FILTERED! " + r.group(0))
                    '''
                    TODO: Currently this is an O(n) operation, as it is nested in another O(n) loop
                    it becomes an O(n^2) operation and is inefficient. Google Python sets and learn why
                    checking for membership is an O(1) operation in a set and an O(n) in a list, then use 
                    a set. Youll have to use .add instead of .append

                    As well, I would add r.group(1) because right now you are able to have duplicates across
                    ats' as their urls will be different but the company name will remain the same.
                    '''
                    if r not in filteredURLs: 
                        filteredURLs.append(r.group(0))
                        companies.write(r.group(1)+"\n")
        #                 nameAndURL[r.group(1)] = r.group(0)          
        # return nameAndURL

    ''' 
    TODO: This is currently hardcoded for lever only, fix that
    '''
    def getJobPosts(self, companyName):
        r = requests.get("https://api.lever.co/v0/postings/" + companyName)
        j = json.loads(r.text)
        return [JobPost(d) for d in j]


if __name__ == "__main__":
    print(WebScraper().getJobPosts("bird"))