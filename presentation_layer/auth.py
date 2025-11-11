from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Cookie, HTTPException, status, Depends, Response, Security
# from fastapi.security import OAuth2PasswordBearer
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from psycopg2.extras import RealDictRow
from database import SingleResult
import service_layer.auth as auth_services
import service_layer.users as user_services
from typing import Annotated
import schemas
import exceptions




auth_router = APIRouter(
    prefix = "/auth",
    tags = ["Authentication"]
)



# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user_from_cookie(
    access_token: Annotated[str | None, Cookie()] = None
):
    credential_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Not Authenticated"
    )
    
    if not access_token:
        raise credential_exception
    
    # Decode the token.
    try:
        
        decoded_token: auth_services.Payload = auth_services.decode_access_token(access_token)
        user_id = decoded_token.get("user_id")

        if not user_id:
            raise credential_exception
        
        user = user_services.fetch_user_by_id(user_id = user_id)
        if not user:
            raise credential_exception

        return schemas.TokenData(
            user_id = user.get("id"),
            role = user.get("role")
        )

    except exceptions.TokenInvalidOrExpiredError:
        raise credential_exception





# def get_current_user(
#     access_token: Annotated[
#         str, 
#         Security(oauth2_scheme)
#     ]
# ) -> schemas.TokenData:

#     # Define credential Exception.
#     credential_exception = HTTPException(
#         status_code = status.HTTP_401_UNAUTHORIZED,
#         detail = "Could not validate your credentials",
#         headers = {
#             "WWW-Authenticate": "Bearer"
#         }
#     )
#     # Decode the token.
#     try:
#         decoded_token: auth_services.Payload = auth_services.decode_access_token(access_token)
#         user_id = decoded_token.get("user_id")

#         if not user_id:
#             raise credential_exception
        
#         user = user_services.fetch_user_by_id(user_id = user_id)

#         if not user:
#             raise credential_exception

#         return schemas.TokenData(
#             user_id = user.get("id"),
#             role = user.get("role")
#         )

#     except exceptions.TokenInvalidOrExpiredError:
#         raise credential_exception



# def get_current_admin(
#     user: Annotated[
#         schemas.TokenData, 
#         Security(get_current_user)
#     ]
# ):

#     if user.role != "admin":
#         raise HTTPException(
#             status_code = status.HTTP_403_FORBIDDEN,
#             detail = "Admin required."
#         )

#     return user


def get_current_admin_from_cookie(
    user: Annotated[
        schemas.TokenData,
        Security(get_current_user_from_cookie)
    ]
):
    if user.role != "admin":
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Admin required"
        )

    return user



@auth_router.post("/login")
async def authenticate(
    form: Annotated[
        OAuth2PasswordRequestForm, 
        Depends()
    ]
):

    try:
        #Authenticate the user.
        authenticated_user: RealDictRow = auth_services.authenticate_user(
            user = schemas.UserLogin(
                email_id = form.username,
                password = form.password
            )
        )

        # Create the access token. 
        access_token: str = auth_services.create_access_token(
            payload = schemas.TokenData(
                user_id = authenticated_user.get("id"),
                role = authenticated_user.get("role")
            )
        )

        # return schemas.Token(
        #     access_token = access_token,
        #     token_type = "Bearer"
        # )
        
        response = Response(content = "You've successfully logged in.", media_type = "text/plain")
        response.set_cookie(
            key = "access_token",
            value = access_token,
            httponly = True,
            samesite = "none",
            secure = True,
            expires = datetime.now(timezone.utc) + timedelta(days = 1)

            # When use in the production. Need to set.
            #samesite = "none", secure = True
        )

        return response

    
    except (exceptions.UserNotFoundError, exceptions.PasswordMismatchError): 
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Incorrect Email or Password."
        )


@auth_router.post("/logout")
async def logout():
    
    response = Response(
        content = "You've logged out successfully",
        media_type = "text/plain"
    )
    
    response.delete_cookie(
        key = "access_token",
        secure = True,
        httponly = True,
        samesite = "none"
    )
    
    return response


@auth_router.get("/me")
async def my_cred_from_cookie(
    user: Annotated[
        schemas.TokenData, 
        Security(get_current_user_from_cookie)
    ]
):

    # Fetch the user details.
    data: SingleResult = user_services.fetch_user_by_id(user.user_id)
    
    return {
        "email_id": data["email_id"],
        "fullname": data["fullname"]
    }



# @auth_router.get("/me")
# async def my_cred_from_header(
#     user: Annotated[
#         schemas.TokenData, 
#         Security(get_current_user)
#     ]
# ):

#     # Fetch the user details.
#     data: SingleResult = user_services.fetch_user_by_id(user.user_id)
    
#     return {
#         "email_id": data["email_id"],
#         "full_name": data["fullname"]
#     }
    
