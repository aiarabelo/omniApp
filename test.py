import requests
import json
from jobPost import JobPost
from googleScrape import WebScraper

companyDetails = {}
# Test company name
companyName = "astranis"
jobPostList = WebScraper().getJobPosts(companyName)  # This is for Lever only
companyDetails[companyName] = [
    [item.commitment, item.title, item.applyUrl] for item in jobPostList
]
jobPostList = list(
    filter(
        lambda x: "Intern" in x[0] and "Software Engineer" in x[1],
        companyDetails[companyName],
    )
)
print([item[2] for item in jobPostList])
