from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from createEngine import createSession, createEngine

engine = createEngine()
Base = declarative_base()

class Company(Base):
  __tablename__ = "companies"
  
  id = Column('id', Integer, primary_key=True) 
  company_name = Column('company_name', String, unique=True)
  ats = Column('ats', String)
  url = Column('url', String)
  
  """
  FUNCTION: Inserts a company's name, ats used, and url into the database
  """
  
  def insert(self, session):
    session.add(self)
    session.commit()
    return self 
  
  """
  FUNCTION: Gets company names
  """
  @classmethod
  def getCompanyNames(cls, session, ats):
    companyName = session.query(Company.company_name).filter(Company.ats==ats).all()    
    return [y[0] for y in companyName]

class CompanyJobs(Base):
  __tablename__ = "job_listings"

  id = Column('id', Integer, primary_key=True)
  company_name = Column('company_name', String, unique=True)
  commitment = Column('commitment', String)
  department = Column('department', String)
  location = Column('location', String)
  team = Column('team', String)
  title = Column('title', String)
  apply_url = Column('apply_url', String, unique=True)
  
  """
  FUNCTION: Inserts the job listings for a company into the table 
  """
  
  def insert(self, session):
    session.add(self)
    session.commit()
    return self 

  """
  FUNCTION: Filters the job listings using desired commitment and job titles
  """  
  def filterJobListings(self, session, commitment, title):
    x = session.query(CompanyJobs.apply_url, CompanyJobs.title).filter(CompanyJobs.commitment.like("%{}%".format(commitment)), CompanyJobs.title.like("%{}%".format(title))).all()
    print(x)
    return [y[0] for y in x]

# session = createSession()
# p = CompanyJobs().filterJobListings(session, commitment="Full time", title="Recruiter")
# print(p)
# session.close()

# session = createSession()
#x   x = Company(company_name="asd", ats="asd", url="asd").insert(session)
# x = CompanyJobs(company_name="asd", commitment="asd", department="asd", location="asd", team="asd", title="asd", apply_url="asd").insert(session)

"""
FUNCTION: Creates "companies" and "job_listings" tables 
"""
session = createSession()
try:
  Company.__table__.create(engine)
  CompanyJobs.__table__.create(engine)
  session.commit()
except: 
  print("Tables already created")
session.close()
