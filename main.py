from fastapi import FastAPI
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
import crud, database, models, schemas
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware 
import datetime

from typing import List


models.Base.metadata.create_all(bind=engine)


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}

#, response_model=List[schemas.Gift]
@app.get("/gifts/")
def read_gifts(db: Session = Depends(get_db)):
    db_gift = crud.get_gifts(db);
   
    return db_gift

@app.get("/users/{username}", response_model=schemas.User)
def read_user(username: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_name(db, username=username)
    return db_user

@app.get("/audits/", response_model=List[schemas.Audit])
def get_audits(db: Session = Depends(get_db)):
    audits = crud.get_audits(db)
    return audits

@app.get("/users/", response_model=List[schemas.User])
def read_users(db: Session = Depends(get_db)):
    users = crud.get_users(db);
    return users

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_name(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    return crud.create_user(db=db, user=user)

@app.post("/users/{username}/gifts/", response_model=schemas.Gift)
def create_gift_for_user(username: str, gift: schemas.GiftCreate, db: Session = Depends(get_db)):
    return crud.create_user_gift(db=db, gift=gift, username=username)

@app.post("/audits/", response_model=schemas.Audit)
def create_audit(audit: schemas.AuditCreate, db: Session = Depends(get_db)):
    return crud.create_audit(db, audit=audit)

@app.put("/users/{username}/role", response_model=schemas.User)
def update_user_role(user: schemas.UserUpdate, username: str, db: Session = Depends(get_db)):
    return crud.update_user(db, username=username, user=user)

@app.delete("/users/{username}/")
def delete_user(username: str, db: Session = Depends(get_db)):
    return crud.delete_user(db, username=username)

@app.delete("/gifts/{giftid}/")
def delete_gift(giftid: int, db: Session = Depends(get_db)):
    return crud.delete_gift(db, gift_id=giftid)

@app.post("/login/")
def login(username: str, password: str, db: Session = Depends(get_db)):
    obj = crud.login(db, username=username, password=password)
    if obj:
        return obj
    else:
        raise HTTPException(status_code=401, detail="Incorrect username or password")