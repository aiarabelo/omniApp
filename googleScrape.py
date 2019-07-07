from googlesearch import search
import time
import re

atsURLs = ['boards.greenhouse.io', 'jobs.lever.co']

class webScraper:
    def companyURL(self, baseURL):
        """
        FUNCTION: Scrapes Google for Company URLs
        companyURL: an unfiltered list of company URLs; these may contain duplicate companies
        baseURL: the base URL of the ATS that will be scraped
        unfilteredURL: URL of company sites that will be scraped in Google
        r: filtered company URL; is of format <baseURL>/company
        Writes the resulting scraped websites onto a different file, of format baseURL.txt
        """
        i = 1
        companyURL = []
        with open(baseURL + ".txt", "a+") as companies:
            for unfilteredURL in search('site:' + atsURL, stop = 25000):
                print(unfilteredURL)
                i+=1
                if i % 10 == 0:
                    time.sleep(60)
                companyURL.append(unfilteredURL)
            for url in companyURL:
                r = re.search(r"https:\/\/jobs\.lever\.co\/[^/]+\/?$", url)
                if r is not None:
                    print("FILTERED! " + r.group(0))
                    companies.write(r.group(0)+"\n")

for atsURL in atsURLs:
    webScraper().companyURL(atsURL)