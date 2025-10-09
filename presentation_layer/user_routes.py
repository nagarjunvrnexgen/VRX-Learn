from fastapi import HTTPException, APIRouter, status
import schemas
import service_layer.users as user_services
import exceptions

user_router = APIRouter(
    prefix ="/users",
    tags = ["Users"] 
)


@user_router.get("/", response_model = list[schemas.User])
async def users():
    return user_services.list_all_users()



@user_router.get("/{user_id}")
async def get_user(user_id: int):
    
    try:
    
        user = user_services.fetch_user_by_id(user_id)
        return user 
    
    except exceptions.UserNotFoundError: 
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"No user found with this Id: {user_id}"
        )
    


@user_router.post("/new", response_model = schemas.User)
async def create_new_user(user: schemas.UserCreate):
   
    try:
       new_user = user_services.register_user(user)
       
       return new_user

    except exceptions.PasswordMismatchError:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Password and confirm password should match!."
        )
    
    except exceptions.EmailAlreadyExist:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "Email already exist with this email id."
        )
    

@user_router.delete("/{user_id}")
async def delete_user(user_id: int):
    try:
        deleted_user =  user_services.remove_user(
            schemas.UserId(id = user_id)
        )
        return deleted_user
    
    except exceptions.UserNotFoundError: 
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "No user found with this Id"
        )
    


