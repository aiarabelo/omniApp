from googlesearch import search
import time

atsURLs = ['boards.greenhouse.io', 'jobs.lever.co']

class webScraper:
    def companyURL(self, baseURL):
        """
        FUNCTION: Fills out the application page
        questionPair: a dictionary containing questions as they key, 
                    and the corresponding WebElements as values
        userData: a dictionary containing the questions as the key, 
                and the answers as valuesH
        Returns questionPair, a dictionary containing questions and its corresponding webelement
        """
        i = 1
        companyURL = []
        with open(baseURL + ".txt", "a+") as companies:
            for unfilteredURL in search('site:' + atsURL, stop = 25000):
                #companies.write(url+"\n")
                i+=1
                if i % 10 == 0:
                    time.sleep(60)
                #for url in unfilteredURL:
                r = re.search(r"https:\/\/jobs\.lever\.co\/[^/]+\/?$", url)
                if r is not None:
                    print(url)
                    companyURL.append(url)
            

                

for atsURL in atsURLs:
    webScraper().companyURL(atsURL)