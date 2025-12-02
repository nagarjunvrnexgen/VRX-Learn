from typing import Annotated
from fastapi import HTTPException, APIRouter, status, Security
import schemas
import service_layer.users as user_services
import exceptions
from presentation_layer.auth import get_current_admin_from_cookie
from fastapi_pagination import Page, paginate



user_router = APIRouter(
    prefix ="/users",
    tags = ["Users"],
    dependencies = [Security(get_current_admin_from_cookie)] 
)


@user_router.get(
    "/", 
    response_model = Page[schemas.User]
)
def get_users():
    return paginate(user_services.list_all_users())



@user_router.get(
    "/{user_id}", 
    response_model = schemas.User
)
def get_user(user_id: int):
    
    try:
    
        user = user_services.fetch_user_by_id(user_id)
        return user 
    
    except exceptions.UserNotFoundError: 
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"User with Id {user_id} does not exist"
        )
    


@user_router.post(
    "/", 
    response_model = schemas.User,
    status_code = status.HTTP_201_CREATED
)
def create_user(user: schemas.UserCreate):
   
    try:
       new_user = user_services.register_user(user)
       
       return new_user

    except exceptions.PasswordMismatchError:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Password and Confirm Password do not match"
        )
    
    except exceptions.EmailAlreadyExist:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = f"Email already exists with this email {user.email_id}"
        )
    

@user_router.delete(
    "/{user_id}",
    status_code = status.HTTP_204_NO_CONTENT
)
def delete_user(user_id: int):
    try:
        
        deleted_user = user_services.remove_user(user_id)
        return
    
    except exceptions.UserNotFoundError: 
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"User with Id {user_id} does not exist"
        )
    
    except exceptions.UserHasDataError:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = f"User with ID {user_id} has associated data and cannot be deleted"
        )


