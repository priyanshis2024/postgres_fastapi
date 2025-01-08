from pydantic import BaseModel,conint,EmailStr,validator
from typing import Optional
from datetime import datetime

class Post(BaseModel):
    Id: Optional[int] = None
    Name: str
    Domain: str
    Age: int
    Email: str
    Is_student: bool = True
    Rating: Optional[int] = None

class Users(BaseModel):
    Id: Optional[int] = None
    Email: EmailStr
    Password: str

class UserOut(BaseModel):
    Id: int
    Email: EmailStr
    Created_at: str

    @validator("Created_at", pre=True)
    def convert_datetime_to_str(cls, value):
        # If value is a datetime object, convert it to ISO 8601 string
        if isinstance(value, datetime):
            return value.isoformat()  # Or any other string format you need
        return value

    class Config:
        orm_mode = True

class Userlogin(BaseModel):
    Email: EmailStr
    Password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class LogoutRequest(BaseModel):
    user_id: int

class Vote(BaseModel):
    post_id : int
    dir: conint(le=1)