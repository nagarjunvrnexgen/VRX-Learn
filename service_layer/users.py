import data_access_layer.users as user_repo
import schemas
from utils import get_hash_password
from database import SingleResult
import exceptions
from psycopg2.extras import RealDictRow



def list_all_users() -> list[RealDictRow]:
    users = user_repo.get_all_users()
    return users
    

def fetch_user_by_id(user_id: int) -> RealDictRow:
    
    user = user_repo.get_user_by_id(id = user_id)

    if not user:
        raise exceptions.UserNotFoundError(
            f"User with ID {user_id} does not exist"
        )
    
    return user



def fetch_user_by_email(
    email_id: str
) -> RealDictRow:
    
    user = user_repo.get_user_by_email(email_id = email_id)

    if not user:
        raise exceptions.UserNotFoundError(
            f"User with email id {email_id} does not exist"
        )
    
    return user


def register_user(
    user: schemas.UserCreate
) -> RealDictRow:
    
     # Check for password mismatch.
    if user.password != user.confirm_password:
        raise exceptions.PasswordMismatchError(
            "Password and Confirm Password do not match"
        )

    # Check for email existance.
    existed_user = user_repo.get_user_by_email(email_id = user.email_id)

    if existed_user:
        raise exceptions.EmailAlreadyExist(
            f"User already found with this Email: {user.email_id}"
        )
    
    # Hash the password.
    user.password = get_hash_password(user.password)

    # Create a new user.
    new_user = user_repo.insert_user(user)

    return new_user



def remove_user(
    id: int
) -> RealDictRow:
    
    deleted_user: SingleResult = user_repo.delete_user(id)

    if not deleted_user:
        raise exceptions.UserNotFoundError(
            f"User with ID {id} does not exist"
        )
    
    return deleted_user












