from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_HOST: str
    REDIS_PORT: int
    AUTH0_DOMAIN: str
    AUTH0_AUDIENCE: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int


    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
