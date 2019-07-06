from googlesearch import search
import time

atsURLs = ['boards.greenhouse.io', 'jobs.lever.co']

class webScraper:
    def companyURL(self, ats):
        i = 1
        with open(ats + ".txt", "a+") as companies:
            for url in search('site:' + atsURL, stop = 25000):
                companies.write(url+"\n")
                i+=1
                if i % 10 == 0:
                    time.sleep(40)
                print("(" + atsURL + ") " +  url)

for atsURL in atsURLs:
    webScraper().companyURL(atsURL)