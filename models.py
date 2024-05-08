from sqlalchemy import create_engine, Column, Integer, BigInteger, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from datetime import datetime


Base = declarative_base()


class User(Base):
	__tablename__ = 'user' 
	id = Column(Integer, primary_key=True)
	username = Column(String(255), unique=True) 
	password = Column(String(2500)) 


class Step(Base):
	__tablename__ = 'step'
	id = Column(Integer, primary_key=True)
	startTime = Column(DateTime)
	startZoneOffset = Column(String(20)) 
	endTime = Column(DateTime)
	endZoneOffset = Column(String(20)) 
	count = Column(Integer)
	stepMetadata  = Column(String(2500)) 

	def __init__(self, startTime, startZoneOffset, endTime, endZoneOffset, count, stepMetadata ):
		self.startTime = startTime
		self.startZoneOffset = startZoneOffset
		self.endTime = endTime
		self.endZoneOffset = endZoneOffset
		self.count = count
		self.stepMetadata = stepMetadata 