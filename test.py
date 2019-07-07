import requests
import json
from jobPost import JobPost
from googleScrape import WebScraper

# Test company name
companyName = "bird"

def getJobPosts(companyName):
    r = requests.get("https://api.lever.co/v0/postings/" + companyName)
    j = json.loads(r.text)
    return [JobPost(d) for d in j]

print([str(item) for item in getJobPosts(companyName)])