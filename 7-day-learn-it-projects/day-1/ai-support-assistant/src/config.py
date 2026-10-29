from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AI Support Assistant"
    admin_email: str
    items_per_user: int = 50


settings = Settings()