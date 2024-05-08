
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Optional, List
import logging
import sys

from os import getenv, path
from dotenv import load_dotenv

from datetime import datetime, timedelta
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from models import Base, User, Step


load_dotenv()
db_config = {
	'host': getenv('DB_HOST'),
	'user': getenv('DB_USER'),
	'password': getenv('DB_PASSWORD'),
	'database': getenv('DB_DATABASE')
}
engine = create_engine(f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}", echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

class UserRequest(BaseModel):
	username: str
	password: str

class StepRequest(BaseModel):
	startTime: datetime
	startZoneOffset: Optional[str] = None 
	endTime: datetime
	endZoneOffset: Optional[str] = None 
	count: int
	stepMetadata: Optional[str] = None

def find_or_insert_user(username: str, password: str) -> bool:
	try:
		with Session() as session:
			db_user = session.query(User).filter_by(username=username).first()
			if db_user is None:
				db_user = User(username=username, password=password)
				session.add(db_user)
				session.flush()			
			session.commit()
			return db_user
	except Exception as e:
		print(f"An error occurred: {e}")
	return None

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/")
async def root():
	return {"message": "Hello World!!!"}



def fetch_all_steps(session):
	return session.query(Step).all()


# def step_exists(steps, step):
# 	for existing_step in steps:
# 		logger.info(str(type(existing_step.startTime)) + " <======> " + str(type(step.startTime)))
# 		if (existing_step.startTime == step.startTime and existing_step.endTime == step.endTime):
# 			return True
# 	return False

def step_exists(steps, step):
	for existing_step in steps:		
		if (existing_step.stepMetadata == step.stepMetadata):
			return True
	return False


@app.post("/api/sync/steps")
async def sync_steps(request: List[StepRequest]):
	try:
		with Session() as session:            
			existing_steps = fetch_all_steps(session)
			# logger.info("existing_steps ======> " + str(existing_steps))
			for step_request in request:
				step = Step(
					startTime=step_request.startTime,
					startZoneOffset=step_request.startZoneOffset,
					endTime=step_request.endTime,
					endZoneOffset=step_request.endZoneOffset,
					count=step_request.count,
					stepMetadata=step_request.stepMetadata
				)                
				if not step_exists(existing_steps, step):
					session.add(step)
					session.flush()
			session.commit() 
			return {"message": "Steps saved successfully."}
	except Exception as e:
		print(f"An error occurred: {e}")
		return {"error": str(e)}











# def saveStep(step: Step):
# 	try:
# 		with Session() as session:			
# 			session.add(step)
# 			session.flush()			
# 			session.commit()
# 			return step
# 	except Exception as e:
# 		print(f"An error occurred: {e}")
# 	return None

# @app.post("/api/sync/steps")
# async def syncSteps(request: StepRequest):
# 	try:
# 		step = Step(
# 			startTime=request.startTime,
# 			startZoneOffset=request.startZoneOffset,
# 			endTime=request.endTime,
# 			endZoneOffset=request.endZoneOffset,
# 			count=request.count,
# 			stepMetadata=request.stepMetadata 
# 		)
# 		print(step)
# 		saveStep(step)
# 		return {"message": "Step saved successfully."}
# 	except Exception as e:
# 		print(f"An error occurred: {e}")
# 		return {"error": str(e)}


@app.post("/api/login")
def login(request_user: UserRequest): 
	try:
		with Session() as session:
			db_user = session.query(User).filter_by(username=request_user.username).first()
			if db_user is None:
				db_user = User(username=request_user.username, password=request_user.password)
				session.add(db_user)
				session.flush()			
			session.commit()
			return {"sessid": str(db_user.id)}
	except Exception as e:
		print(f"An error occurred: {e}")
		raise HTTPException(status_code=400, detail="exception in try")

