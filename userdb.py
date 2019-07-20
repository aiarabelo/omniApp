import psycopg2

def insertCompanyInfo(company_name, ats, url):
        conn = psycopg2.connect(host="localhost", database = "omniApp", user = "postgres", password = "l1pt0n")
        cur = conn.cursor()
        cur.execute("INSERT INTO companies (company_name, ats, url) VALUES (%s,%s,%s)", ('company_name', 'ats', 'url'))
        id = cur.fetchone()[0]
        conn.commit()
        cur.close()
insertCompanyInfo("company", "ats", "url")

conn = psycopg2.connect(host="localhost", database = "omniApp", user = "postgres", password = "l1pt0n")
cur = conn.cursor()
# insert_query = """ INSERT INTO mobile (ID, MODEL, PRICE) VALUES (%s,%s,%s)"""  
# record_to_insert = (5, 'One Plus 6', 950)
# cursor.execute(postgres_insert_query, record_to_insert)

x = cur.execute("SELECT * FROM companies")
print(x)
print(conn)
print(cur)