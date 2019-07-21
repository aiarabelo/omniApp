import psycopg2


class Company:
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
    
    def getCompanyNames(self, ats):
        conn = psycopg2.connect(host="localhost", database = "omniApp", user = "postgres", password = "l1pt0n")
        cursor = conn.cursor()
        
        cursor.execute(""" SELECT company_name FROM companies WHERE ats = %s""", (ats,))
        
        company_names = [company_name[0] for company_name in cursor.fetchall()]

        cursor.close()
        conn.close()
    
        return company_names
