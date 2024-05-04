
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from os import getenv, path
from dotenv import load_dotenv

from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User


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



class UserPydantic(BaseModel):
    username: str
    password: str



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


@app.get("/")
async def root():
	# save_user("John", "123")
	return {"message": "Hello World"}


@app.post("/api/sync/{method}")
async def sync(method):
	try:
		# method = method[0].lower() + method[1:]
		print(method)
		method_str = str(method)	
		# save_user("John", method_str)
		userid = request.json['userid']
		data = request.json['data']
		if type(data) != list:
			data = [data]
		print(method, len(data))
		return method_str
	except Exception as e:
		print(f"An error occurred: {e}")
	return "error"


	


@app.post("/api/login")
def login(request_user: UserPydantic): 
	try:
		with Session() as session:
			db_user = session.query(User).filter_by(username=request_user.username).first()
			if db_user is None:
				db_user = User(username=request_user.username, password=request_user.password)
				session.add(db_user)
				session.flush()			
			session.commit()
			return {"sessid": db_user.id}
	except Exception as e:
		print(f"An error occurred: {e}")
		raise HTTPException(status_code=400, detail="exception in try")

