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