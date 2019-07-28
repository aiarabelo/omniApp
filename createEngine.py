from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import psycopg2
import json


# env.json contains database details
with open("env.json", "r") as f:
  credentials = json.loads(f.read())

def createEngine():
  engine = create_engine("postgresql://"+credentials["DATABASE_USER"]+":"+credentials["DATABASE_PASSWORD"]+"@"+credentials["DATABASE_HOST"]+"/"+credentials["DATABASE_NAME"], echo=True)
  return engine

def createSession():
  engine = createEngine()
  Session = sessionmaker(bind=engine)
  session = Session()
  return session
