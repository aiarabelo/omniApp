from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String

engine = create_engine('sqlite:///:memory:', echo=True) # Set echo to false if you want less output generated 
Base = declarative_base()

class User(Base):
      __tablename__ = "userData" 

      id = Column(Integer, primary_key=True)
      resume = Column(String)
      fullname = Column(String) #Set nullable = False? 
      email = Column(String)
      phone = Column(String)
      current_company = Column(String)
      twitter = Column(String)
      linkedin = Column(String)
      github = Column(String)
      portfolio = Column(String)
      other_site = Column(String)
      legal_age = Column(String)
      work_authorization_status = Column(String) 
      sponsorship_requirements = Column(String)
      start_date = Column(String)
      referred = Column(String)
      languages = Column(String)
      hear_about_job = Column(String)
      gender = Column(String)
      race = Column(String)
      veteran_status = Column(String)
      certify = Column(String)
      disability = Column(String)

      def __repr__(self):
            return "<resume='%s', fullname='%s', email='%s', phone='%s', current_company='%s', twitter='%s',\
                  linkedin='%s', github='%s', portfolio='%s', other_site='%s', legal_age='%s', work_authorization_status='%s'\
                  sponsorship_requirements='%s', start_date='%s', referred='%s',languages='%s', hear_about_job='%s'\
                  gender='%s', race='%s', veteran_status='%s', certify='%s', disability='%s'> % (self.resume, self.fullname\
                  self.email, self.phone, self.current_company, self.twitter, self.linkedin, self.github, self.portfolio,\
                  self.other_site, self.legal_age, self.work_authorization_status, self.sponsorship_requirements, \
                  self.start_date, self.referred, self.languages, self.hear_about_job, self.gender, self.race, \
                  self.veteran_status, self.certify, self.disability)"

#TODO: Short answer questions
#TODO: Join table with a variation of all questions (from scraping)
#TODO: For disability, if input indicates disability:
      #make input name be full name and date the current date

print(User.__table__)


# TODO: Don't hardcode this, put it in env.json or make a fake wrapper
# for a database and just make it return this for now



print(userData)