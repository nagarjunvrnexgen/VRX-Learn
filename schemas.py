from pydantic import BaseModel, EmailStr
from typing import Literal
from datetime import datetime



class UserBase(BaseModel):
    fullname: str
    email_id: EmailStr
    role: Literal["trainee", "admin"]


class UserCreate(UserBase):    
    password: str 
    confirm_password: str 


class User(UserBase):
    id: int
    # password: str
    created_at: datetime


class UserUpdate(BaseModel):
    email_id: EmailStr
    password: str




class UserLogin(BaseModel):
    email_id: str
    password: str



class TokenData(BaseModel):
    user_id: int
    role: Literal["trainee", "admin"]

class Token(BaseModel):
    access_token: str 
    token_type: str = "Bearer"

# """
# =========================================================================================
#                 Courses Schema
# =========================================================================================
# """



class CourseCreate(BaseModel):
    name: str 
    description: str 
    author: str


class Course(CourseCreate):
    id: int 
    created_at: datetime



    
class ModuleCreate(BaseModel):
    name: str 
    course_id: int 



class Module(ModuleCreate):
    id: int 
    created_at: datetime


class ResourceCreate(BaseModel):
    name: str 
    type: Literal["pdf", "video"]
    file_type: Literal[".pdf", ".mp4"]
    url: str 
    module_id: int



class Resource(ResourceCreate):
    id: int 
    created_at: datetime
    

class EnrollmentCreate(BaseModel):

    user_id: int
    course_id: int


class EnrollmentLookUp(EnrollmentCreate):
    pass


class Enrollment(EnrollmentCreate):
    id: int 
    enrolled_at: datetime


class EnrollmentAggregated(BaseModel):
    id: int
    user_id: int
    username: str
    course_id: int
    course_name: str
    enrolled_at: datetime


