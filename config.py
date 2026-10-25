from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str = ''
    DB_PORT: str = ''
    DB_NAME: str = ''
    DB_USER: str = ''
    DB_PASS: str = ''

    model_config = SettingsConfigDict(env_file='.env')

    @property
    def async_db_dns(self):
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'


def get_settins():
    return Settings()

settings = get_settins()