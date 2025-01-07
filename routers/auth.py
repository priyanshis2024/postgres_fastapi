from fastapi import FastAPI,Depends,HTTPException,status,APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import models,utils
from app.database import get_db
from app import oauth2
from app import schemas
# from app.utils import pwd_context,verify_password
from datetime import datetime,timedelta
from app import session
from typing import List
from app.session import get_all_logged_in_users,logout
from app.schemas import LogoutRequest

router = APIRouter(tags=["Authentication"])

@router.get("/login")
# @router.post("/login",response_model=schemas.Token)
# def login(user_credentials: schemas.Userlogin,db: Session = Depends(get_db)):
def login(user_credentials: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    # user = db.query(models.User).filter(models.User.Email == user_credentials.Email).first()
    user = db.query(models.User).filter(
        models.User.Email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"User with email {user_credentials.Email} not found!!")
    
    if not utils.verify_password(user_credentials.password,user.Password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")
    
    # create token
    # return token

    access_token = oauth2.create_access_token(data={"user_id":user.Id})
    return {"access_token":access_token,"token_type":"bearer"}

    # return {"message":"Login successful!!"}

@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Authenticate user by querying the database
    user = db.query(models.User).filter(models.User.Email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    if not utils.verify_password(user_credentials.password, user.Password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    # Create the access token
    access_token = oauth2.create_access_token(data={"user_id": user.Id})

    # Define expiration time for the session (e.g., 30 minutes)
    expires_at = datetime.utcnow() + timedelta(minutes=30)

    # Store the active session in the database
    active_session = models.ActiveSession(
        user_id=user.Id, 
        token=access_token, 
        expires_at=expires_at
    )
    db.add(active_session)
    db.commit()
    db.refresh(active_session)

    return {"access_token": access_token, "token_type": "bearer"}


# Logout endpoint
@router.post("/logout")
def user_logout(request: LogoutRequest, db: Session = Depends(get_db)):
    # Log the user out by removing their session
    logout(request.user_id, db)
    return {"message": "User logged out successfully"}

# Get all logged-in users endpoint
@router.get("/active-users", response_model=List[int])  # List of user_ids of logged-in users
def active_users(db: Session = Depends(get_db)):
    # Fetch all logged-in users
    active_users = get_all_logged_in_users(db)
    return active_users
