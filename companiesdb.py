import psycopg2


class Company:
    """
    FUNCTION: Creates "companies" database, and inserts a company's name, ats used, and url into the database
    company_name: name of the company, corresponding to what's used in the URL
    ats: ATS used by the site (Greenhouse, Lever)
    url: URL of the company on the ats
    """
    def insertInfo(self, company_name, ats, url):
        conn = psycopg2.connect(host="localhost", database = "omniApp", user = "postgres", password = "l1pt0n")
        cursor = conn.cursor()
        #cursor.execute("DROP TABLE IF EXISTS companies;")
        cursor.execute("""CREATE TABLE IF NOT EXISTS companies (
            id SERIAL PRIMARY KEY,
            company_name TEXT UNIQUE,
            ats TEXT, 
            url TEXT    
        )""")
        
        cursor.execute("""INSERT INTO companies (company_name, ats, url) VALUES (%s, %s, %s)""", (company_name, ats, url))
        
        # cursor.execute("SELECT * FROM companies")
        # print(cursor.fetchall())

        conn.commit()
        cursor.close()
        conn.close()
    """
    FUNCTION: Retrieves company names from the database based on the ats used
    returns company_names, a list of company names on an ATS
    """
    
    def getCompanyNames(self, ats):
        conn = psycopg2.connect(host="localhost", database = "omniApp", user = "postgres", password = "l1pt0n")
        cursor = conn.cursor()
        
        cursor.execute(""" SELECT company_name FROM companies WHERE ats = %s""", (ats,))
        
        company_names = [company_name[0] for company_name in cursor.fetchall()]

        cursor.close()
        conn.close()
    
        return company_names
