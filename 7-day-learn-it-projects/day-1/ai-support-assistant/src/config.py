from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Support Assistant"
    admin_email: str
    azure_openai_endpoint: str
    azure_openai_api_key: str
    azure_openai_chat_deployment: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")




    


settings = Settings()