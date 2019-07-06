from googlesearch import search
import time

atsURLS = ['boards.greenhouse.io', 'jobs.lever.co']

class webScraper:
    def companyURL(self, atsURL):
        i = 1
        with open(atsURL + ".txt", "a+") as companies:
            for url in search('site:' + atsURL, stop = 20000):
                companies.write(url+"\n")
                i+=1
                if i % 10 == 0:
                    time.sleep(40)
                print(url)

print(webScraper().companyURL(atsURLS[0]))
