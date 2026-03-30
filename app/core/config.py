from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "API Python HotelBooking"
    APP_ENV: str = "development"
    DATABASE_URL: str = "sqlite:///./hotel.db"

    class Config:
        env_file = ".env"

settings = Settings()