import os
from googleScrape import WebScraper

if __name__ == "__main__":
    # Scrapes Google for companies on Lever if the .txt file of scraped URLs doesn't exist yet
    if not os.path.exists("./jobs.lever.co.txt"):
        WebScraper().companyInfo("jobs.lever.co")
    with open("jobs.lever.co.txt", r)