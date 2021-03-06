from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    DATABASE_URL: str
    SERVER_ORIGIN: str = "https://directory.org.ua"

    @validator("DATABASE_URL", pre=True)
    def normalize(cls, database_url: str) -> str:
        if isinstance(database_url, str) and database_url.startswith("postgres://"):
            return "postgresql://" + database_url.removeprefix("postgres://")
        return database_url


settings = Settings()
