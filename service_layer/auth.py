import data_access_layer.users as user_repo
import schemas
import exceptions
import utils
from datetime import datetime, timedelta, timezone
import jwt
from configs import settings
from typing import TypedDict



def authenticate_user(user: schemas.UserLogin):

    # Check for user existance.
    requested_user = user_repo.get_user_by_email(user.email_id)

    if not requested_user:
        raise exceptions.UserNotFoundError(
            "No user found with this Email."
        )
    
    # Check for password.
    if not utils.verify_hash_password(user.password, requested_user.get("password", "")):
        raise exceptions.PasswordMismatchError(
            "Incorrect password"
        )
    
    return requested_user




def create_access_token(
    payload: schemas.TokenData, 
    expires_delta: timedelta | None = None
):
    
    data = payload.model_dump().copy()

    if expires_delta:
        expires = datetime.now(timezone.utc) + expires_delta
    else:
        expires = datetime.now(timezone.utc) + timedelta(minutes = settings.jwt_token_expire_minutes)

    # Update the payload with subject and expiration time of  the token.
    data.update(
        {
            "sub": "access_token",
            "exp": expires
        }
    )

    encoded_jwt = jwt.encode(
        data, key = settings.jwt_secret_key,
        algorithm = settings.algorithm
    )

    return encoded_jwt




class Payload(TypedDict):
    user_id: int
    role: str
    sub: str
    exp: int 



def decode_access_token(token: str) -> dict:

    try:
        payload: Payload = jwt.decode(
            token, key = settings.jwt_secret_key,
            algorithms = [settings.algorithm]
        )

        return payload

    except jwt.PyJWTError:
        raise exceptions.TokenInvalidOrExpiredError()




