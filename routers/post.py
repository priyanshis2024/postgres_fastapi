from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from typing import List,Optional
from app import models,schemas,oauth2
from app.database import get_db
from app.schemas import Post
# from app.oauth2 import get_current_user

router = APIRouter()
# router = APIRouter(prefix="/post", tags=["Post"])
# Test SQLAlchemy
@router.get("/sqlalchemy")
def test_sqlalchemy(db: Session = Depends(get_db)):
    db.query(models.PostModel).all()
    # print(x)
    # return {"Data":x}
    return {"status":"SQLAlchemy is working fine!! Success!!"}

# Create a new post
@router.post("/posts",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
# def create_post(post: Post,db: Session = Depends(get_db),user_id: int = Depends(oauth2.get_current_user)):
def create_post(post: Post,db: Session = Depends(get_db)):

    # print(user_id)

# def create_post(post: Post,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # print(current_user)
    new_post = models.PostModel(Name=post.Name,Domain=post.Domain,Age=post.Age,Email=post.Email,Is_student=post.Is_student,Rating=post.Rating)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# Get all posts
@router.get("/posts",response_model=List[schemas.Post])
# def get_posts(db: Session = Depends(get_db),user_id: int = Depends(oauth2.get_current_user),
#               limit: int = 10, skip: int = 0, search: Optional[str]=""):
def get_posts(db: Session = Depends(get_db),user_id: int = Depends(get_db),
              limit: int = 10, skip: int = 0, search: Optional[str]=""):
    # posts = db.query(models.PostModel).all()
    # return posts

    query = db.query(models.PostModel)

    # Apply search filter if search term is provided
    if search:
        query = query.filter(models.PostModel.Email.ilike(f"%{search}%"))

    # Apply pagination
    query = query.offset(skip).limit(limit)

    # Fetch the posts
    posts = query.all()
    return posts

# Get a post by Id
@router.get("/posts/{post_id}",response_model=schemas.Post)
def get_post_id(post_id: int, db: Session = Depends(get_db)):
    post_id = db.query(models.PostModel).filter(models.PostModel.Id == post_id).first()
    
    if not post_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id {post_id} not found!!")
    return post_id

# Update a post by Id
@router.put("/posts/{post_id}",response_model=schemas.Post)
# def update_post(post_id: int,post: Post,db: Session = Depends(get_db),user_id: int = Depends(oauth2.get_current_user)):
def update_post(post_id: int,post: Post,db: Session = Depends(get_db),user_id: int = Depends(get_db)): # without authentication of user login or not

    post_to_update = db.query(models.PostModel).filter(models.PostModel.Id == post_id).first()
    post_to_update.Name = post.Name
    post_to_update.Domain = post.Domain
    post_to_update.Age = post.Age
    post_to_update.Email = post.Email
    post_to_update.Is_student = post.Is_student
    post_to_update.Rating = post.Rating
    db.commit()
    db.refresh(post_to_update)
    # print(post_to_update)  # This will print the update query
    return post_to_update

@router.delete("/posts/{post_id}", response_model=schemas.Post)
# def delete_post(post_id: int, db: Session = Depends(get_db),user_id: int = Depends(oauth2.get_current_user)):
def delete_post(post_id: int, db: Session = Depends(get_db),user_id: int = Depends(get_db)):

    post = db.query(models.PostModel).filter(models.PostModel.Id == post_id).first()    
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found!!")
    db.delete(post)
    db.commit()

    return post