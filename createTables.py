from models import Company, CompanyJobs
from createEngine import createEngine
from sqlalchemy.ext.declarative import declarative_base


engine = createEngine()

Base = declarative_base()
Base.metadata.create_all(bind=engine)