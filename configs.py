from pydantic_settings import BaseSettings



class Settings(BaseSettings):

    database_name: str 
    database_host: str 
    database_password: str 
    database_user: str
    database_port: int 


    class Config:
        env_file = ".env"
        extras = "ignore"



settings = Settings()
print("API Keys Initialized Successfully.")
