with open("jobs.lever.co.txt", "r") as f:
    print("Extracting company names from Lever...")
    leverCompanyNames = f.read().split("\n")
    print("Extraction done!")

leverCompanyNames = leverCompanyNames[:-1]
print(leverCompanyNames)