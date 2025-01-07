from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from typing import List
from app import models,schemas,utils
from app.database import get_db
from app.utils import pwd_context

router = APIRouter()

# Create a new user (Insert a new user in the database)
@router.post("/users",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user:schemas.Users,db: Session = Depends(get_db)):
    
    # hashing the password
    # hashed_password = pwd_context.hash(user.Password)
    hashed_password = utils.hash(user.Password)
    user.Password = hashed_password

    new_user = models.User(Id=user.Id,Email=user.Email,Password=user.Password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Get all posts
@router.get("/users",response_model=List[schemas.Users])
def get_user(db: Session = Depends(get_db)):
    all_user = db.query(models.User).all()
    return all_user

# Get a user by Id
@router.get("/users/{user_id}",response_model=schemas.UserOut)
def get_user_id(user_id: int, db: Session = Depends(get_db)):
    user_id = db.query(models.User).filter(models.User.Id == user_id).first()
    
    if not user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id {user_id} not found!!")
    
    return user_id

# Delete a user by Id
@router.delete("/users/{user_id}")
def delete_user(user_id: int,db: Session = Depends(get_db)):
    user_to_delete = db.query(models.User).filter(models.User.Id == user_id).first()
    db.delete(user_to_delete)
    db.commit()
    return {"message":"User deleted successfully!!"}

# Insert multiple users
@router.post("/users/bulk",status_code=status.HTTP_201_CREATED)
def insert_bulk_users(users: List[schemas.Users],db: Session = Depends(get_db)):
    for user in users:
        hashed_password = utils.hash(user.Password)
        user.Password = hashed_password
        new_user = models.User(Id=user.Id,Email=user.Email,Password=user.Password)
        db.add(new_user)
    db.commit()
    return {"message":"Bulk users inserted successfully!!"}