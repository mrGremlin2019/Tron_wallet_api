from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODE: str # Для тестовой БД

    DATABASE_URL: str

    @property
    def DB_URL(self):
        return f"sqlite:///./{self.DATABASE_URL}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
