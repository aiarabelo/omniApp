import psycopg2
import json

# env.json contains database details
with open("env.json", "r") as f:
    credentials = json.loads(f.read())


class Company:
    def __init__(self):
        conn = psycopg2.connect(
            host=credentials["DATABASE_HOST"],
            database=credentials["DATABASE_NAME"],
            user=credentials["DATABASE_USER"],
            password=credentials["DATABASE_PASSWORD"],
        )
        cursor = conn.cursor()

        cursor.execute(
            """CREATE TABLE IF NOT EXISTS companies (
            id SERIAL PRIMARY KEY,
            company_name TEXT UNIQUE,
            ats TEXT, 
            url TEXT    
        )"""
        )

        conn.commit()
        cursor.close()
        conn.close()

    """
    FUNCTION: Creates "companies" database, and inserts a company's name, ats used, and url into the database
    company_name: name of the company, corresponding to what's used in the URL
    ats: ATS used by the site (Greenhouse, Lever)
    url: URL of the company on the ats
    """

    def insertInfo(self, company_name, ats, url):
        conn = psycopg2.connect(
            host=credentials["DATABASE_HOST"],
            database=credentials["DATABASE_NAME"],
            user=credentials["DATABASE_USER"],
            password=credentials["DATABASE_PASSWORD"],
        )
        cursor = conn.cursor()

        cursor.execute(
            """INSERT INTO companies (company_name, ats, url) VALUES (%s, %s, %s)""",
            (company_name, ats, url),
        )

        conn.commit()
        cursor.close()
        conn.close()

    """
    FUNCTION: Retrieves company names from the database based on the ats used
    returns company_names, a list of company names on an ATS
    """

    def getCompanyNames(self, ats):
        conn = psycopg2.connect(
            host=credentials["DATABASE_HOST"],
            database=credentials["DATABASE_NAME"],
            user=credentials["DATABASE_USER"],
            password=credentials["DATABASE_PASSWORD"],
        )
        cursor = conn.cursor()

        cursor.execute(""" SELECT company_name FROM companies WHERE ats = %s""", (ats,))

        company_names = [company_name[0] for company_name in cursor.fetchall()]

        conn.commit()
        cursor.close()
        conn.close()

        return company_names


class CompanyJobs:
    def __init__(self):
        conn = psycopg2.connect(
            host=credentials["DATABASE_HOST"],
            database=credentials["DATABASE_NAME"],
            user=credentials["DATABASE_USER"],
            password=credentials["DATABASE_PASSWORD"],
        )
        cursor = conn.cursor()

        cursor.execute(
            """CREATE TABLE IF NOT EXISTS job_listings (
            id SERIAL PRIMARY KEY,
            company_name TEXT,
            commitment TEXT,
            department TEXT, 
            location TEXT,
            team TEXT,    
            title TEXT,
            apply_url TEXT UNIQUE
        )"""
        )
        conn.commit()
        cursor.close()
        conn.close()

    def insertJobListings(
        self, company_name, commitment, department, location, team, title, apply_url
    ):
        conn = psycopg2.connect(
            host=credentials["DATABASE_HOST"],
            database=credentials["DATABASE_NAME"],
            user=credentials["DATABASE_USER"],
            password=credentials["DATABASE_PASSWORD"],
        )
        cursor = conn.cursor()

        cursor.execute(
            """INSERT INTO job_listings (company_name, commitment, department, location, team, title, apply_url) VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (company_name, commitment, department, location, team, title, apply_url),
        )

        conn.commit()
        cursor.close()
        conn.close()

    # def filterCompanies(self, com):
    #     conn = psycopg2.connect(
    #         host=credentials["DATABASE_HOST"],
    #         database=credentials["DATABASE_NAME"],
    #         user=credentials["DATABASE_USER"],
    #         password=credentials["DATABASE_PASSWORD"],
    #     )
    #     cursor = conn.cursor()

    #     cursor.execute(
    #         """SELECT company_name, apply_url FROM job_listings 
    #             WHERE commitment = (%s) AND title = (%s) AND location LIKE (%s)""",
    #         (commitment, title, location),
    #     )

    #     conn.commit()
    #     cursor.close()
    #     conn.close()
