import psycopg2
import json

# env.json contains database details
with open("env.json", "r") as f:
    credentials = json.loads(f.read())
conn = psycopg2.connect(host=credentials["DATABASE_HOST"], database = credentials["DATABASE_NAME"], user = credentials["DATABASE_USER"], password = credentials["DATABASE_PASSWORD"])
cursor = conn.cursor()

class Company:
    """
    FUNCTION: Creates "companies" database, and inserts a company's name, ats used, and url into the database
    company_name: name of the company, corresponding to what's used in the URL
    ats: ATS used by the site (Greenhouse, Lever)
    url: URL of the company on the ats
    """
    def insertInfo(self):
        cursor.execute("""CREATE TABLE IF NOT EXISTS companies (
            id SERIAL PRIMARY KEY,
            company_name TEXT UNIQUE,
            ats TEXT, 
            url TEXT    
        )""")
        
        cursor.execute("""INSERT INTO companies (company_name, ats, url) VALUES (%s, %s, %s)""", (company_name, ats, url))
        
        cursor.execute("SELECT * FROM companies")
        print(cursor.fetchall())

        conn.commit()
        cursor.close()
        conn.close()

    """
    FUNCTION: Retrieves company names from the database based on the ats used
    returns company_names, a list of company names on an ATS
    """
    def getCompanyNames(self, ats):
        connectToDB()
        
        cursor.execute(""" SELECT company_name FROM companies WHERE ats = %s""", (ats,))
        
        company_names = [company_name[0] for company_name in cursor.fetchall()]

        cursor.close()
        conn.close()
    
        return company_names

#cursor.execute("DROP TABLE IF EXISTS companies;")