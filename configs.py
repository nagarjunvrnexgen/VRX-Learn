from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, Field



class DatabaseSettings(BaseSettings):
    
    user: str 
    name: str 
    password: str 
    host: str 
    port: int

    model_config = SettingsConfigDict(
        env_prefix = "DATABASE_",
        extra = "ignore",
        env_file = ".env"
    )


class JWTSettings(BaseSettings):
    secret_key: str 
    token_expire_minutes: int 
    algorithm: str

    model_config = SettingsConfigDict(
        env_prefix = "JWT_",
        extra = "ignore",
        env_file = ".env"
    )


class GoogleCredentialSettings(BaseSettings):
    type: str 
    project_id: str
    private_key_id: str 
    private_key: str
    client_id: str
    client_email: str
    auth_uri: str
    token_uri: str
    auth_provider_x509_cert_url: str
    client_x509_cert_url: str
    universe_domain: str

    model_config = SettingsConfigDict(
        env_prefix = "GOOGLE_",
        env_file = ".env",
        extra = "ignore"
    )


class CORSSettings(BaseSettings):
    
    allowed_origins: list[str]
    
    model_config = SettingsConfigDict(
        env_file = ".env",
        env_prefix = "CORS_",
        extra = "ignore"
    )
    

class Settings(BaseModel):

    database: DatabaseSettings = Field(default_factory = DatabaseSettings)
    jwt: JWTSettings = Field(default_factory = JWTSettings)
    google_credentials: GoogleCredentialSettings = Field(default_factory = GoogleCredentialSettings)
    cors: CORSSettings = Field(default_factory = CORSSettings)

settings = Settings()
print("API Keys Initialized Successfully.")
