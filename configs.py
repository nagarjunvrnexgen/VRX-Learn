from pydantic_settings import BaseSettings



class Settings(BaseSettings):

    database_name: str 
    database_host: str 
    database_password: str 
    database_user: str
    database_port: int 

    jwt_secret_key: str
    jwt_token_expire_minutes: int 
    algorithm: str = "HS256"


    class Config:
        env_file = ".env"
        extras = "ignore"



settings = Settings()
print("API Keys Initialized Successfully.")
