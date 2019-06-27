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
      fullname = Column(String)
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



userData = {
      "Resume/CV" : "C:/Users/aiarabelo/Desktop/Projects/OmniApp/resume.pdf",
      "Full name" : "Allison Arabelo",
      "Email" : "arabelo.aa@gmail.com",
      "Phone" : "628-241-9814",
      "Current company" : "Enishi.ai",
      "Twitter URL" : "",
      "LinkedIn URL" : "https://www.linkedin.com/in/allisonarabelo/",
      "GitHub URL" : "https://www.github.com/aiarabelo", 
      "Portfolio URL" : "http://www.allisonarabelo.com/",
      "Other website" : "",
      "At the time of applying, are you 18 years of age or older?" : "Yes",
      "Are you legally authorized to work in the United States?" : "No",
      "Are you legally authorized to work in the country for which you are applying" : "No",
      "Are you currently authorized to work in the U.S.?" : "No",
      "Will you now or in the future require Rigetti Quantum Computing to commence (\"sponsor\") an immigration case in order to employ you?" : "Yes",
      "Will you now or in the future require sponsorship for employment visa status e g H 1B etc" : "Yes",
      "Will you now or in the future require sponsorship for employment visa status" : "Yes",
      "When are you seeking to begin a full-time position?" : "Immediately", 
      "Do you currently, or in the future will you, require sponsorship to legally work in the United States?" : "Yes",
      "Were you referred to Rigetti?" : ["Yes"], 
      "If so, by whom?" : "Daniel Setiawan",
      "Language Skill s Check all that apply" : ["English (ENG)"],
      "Where are you applying from" : "United States [USA]",
      "How did you hear about this job?" : "LinkedIn",
      "Please tell us how you heard about this opportunity" : "Other",
      "What has been your favorite project or proudest accomplishment Why" : "TEST TEST TEST",
      "Gender" : "Female",
      "Race" : "Asian (Not Hispanic or Latino)",
      "Veteran status" : "I am not a protected veteran",
      "I certify the information and answers provided by me within this application are true and correct." : "I Accept / I Agree",
      "Disability status" : "No, I don't have a disability"
}