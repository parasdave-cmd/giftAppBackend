from sqlalchemy.orm import Session
import models, schemas
import datetime

def get_gifts(db: Session):
    return db.query(models.Gifts).all()

def get_users(db: Session):
    return db.query(models.Users).all()

def get_audits(db: Session):
    return db.query(models.Audits).all()

def get_user_by_name(db: Session, username: str):
    return db.query(models.Users).filter(models.Users.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password
    db_user = models.Users(username=user.username, hashed_password=fake_hashed_password, is_admin=user.is_admin)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_user_gift(db: Session, gift: schemas.GiftCreate, username: str):
    db_item = models.Gifts(**gift.dict(), owner_name=username)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def create_audit(db: Session, audit: schemas.AuditCreate):
    db_audit = models.Audits(action = audit.action, object=audit.object, time=datetime.datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S"))
    db.add(db_audit)
    db.commit()
    db.refresh(db_audit)
    return db_audit

def update_user(db: Session, user: schemas.UserUpdate, username: str):
    db_user = db.query(models.Users).filter(models.Users.username == username).one_or_none()
    if db_user is None:
        return None
    for key, value in user.dict().items():
        if key=="is_admin":
            print("is admin", key, value)
            setattr(db_user, "is_admin", value) #if value else None
            
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, username: str):
    db_user = db.query(models.Users).filter(models.Users.username == username).one_or_none()
    db.delete(db_user)
    db.commit()
    return {"deleted": True}

def delete_gift(db:Session, gift_id: int):
    db_gift = db.query(models.Gifts).filter(models.Gifts.id == gift_id).one_or_none()
    db.delete(db_gift)
    db.commit()
    return {"deleted": True}

def login(db: Session, username: str, password: str):
    db_user = db.query(models.Users).filter(models.Users.username == username).one_or_none()
    if db_user is None:
        return None
    if db_user.hashed_password == password:
        return {"token": "1234567890", "username": db_user.username}
    else:
        return None


