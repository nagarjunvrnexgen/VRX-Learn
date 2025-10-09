import data_access_layer.users as user_repo
import schemas
from utils import get_hash_password
from database import SingleResult
import exceptions


def list_all_users():
    users = user_repo.get_all_users()
    return users
    

def fetch_user_by_id(user_id: int):
    user = user_repo.get_user(
        schemas.UserGetById(id = user_id)
    )

    if not user:
        raise exceptions.UserNotFoundError(
            f"No User found with this ID: {user_id}"
        )
    
    return user



def fetch_user_by_email(email_id: str):
    user = user_repo.get_user(
        schemas.UserGetByEmail(
            email_id = email_id
        )
    )

    if not user:
        raise exceptions.UserNotFoundError(
            f"No User found with this email id: {email_id}"
        )
    
    return user


def register_user(user: schemas.UserCreate):
    
     # Check for password mismatch.
    if user.password != user.confirm_password:
        raise exceptions.PasswordMismatchError(
            "Password and confirm password mismatch"
        )

    # Check for email existance.
    existed_user = user_repo.get_user(
        schemas.UserGetByEmail(
            email_id = user.email_id
        )
    )

    if existed_user:
        raise exceptions.EmailAlreadyExist(
            "User already found with this Email."
        )
    
    # Hash the password.
    user.password = get_hash_password(user.password)

    # Create a new user.
    new_user = user_repo.insert_user(user)

    return new_user



def remove_user(user: schemas.UserId):
    
    deleted_user: SingleResult = user_repo.delete_user(user)

    if not deleted_user:
        raise exceptions.UserNotFoundError(
            "No user found with this ID"
        )
    
    return deleted_user












