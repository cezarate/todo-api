"""This is the settings file.
It manages the application's environment variables.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """This is the Settings class
    It is responsible for loading the enviornment variables of 
    the application saved in the .env file.

    Attributes:
    db_name -- The name of the database
    """

    db_name: str

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

settings = Settings()
