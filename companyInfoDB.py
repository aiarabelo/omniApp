from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import psycopg2
import json
from createEngine import engine, session


# env.json contains database details
with open("env.json", "r") as f:
  credentials = json.loads(f.read())

Base = declarative_base()



class Company(Base):
  __tablename__ = "test"
  
  id = Column('id', Integer, primary_key=True) 
  company_name = Column('company_name', String, unique=True)
  ats = Column('ats', String)
  url = Column('url', String)

  
  # def insertInfo(self, company_name, ats, url):

Base.metadata.create_all(bind=engine)
# x = Company(company_name = "sdsa", ats = "asd", url="asdasd")
# session.add(x)
# session.commit()
# session.close()

engine.execute("INSERT INTO test (company_name, ats, url) VALUES ('asd', 'Asd', 'asd')")

# session.add()
# conn = engine.connect()

# conn.execute("""CREATE table test (id SERIAL PRIMARY KEY,
#             company_name TEXT UNIQUE,
#             ats TEXT, 
#             url TEXT)""")
# conn.execute("commit")
# conn.close()