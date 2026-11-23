from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Settings(BaseSettings):
    app_name: str = "AI Support Assistant"
    admin_email: str
    azure_openai_endpoint: str
    azure_openai_api_key: SecretStr
    azure_openai_chat_deployment: str
    azure_openai_embedding_deployment: str
    docs_dir: str = "docs"
    prompts_dir: str = "prompts"
    vector_store_dir: str
    chunk_size: int = 1000
    chunk_overlap: int = 150
    top_k: int = 4
    SecretStr: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")




    


settings = Settings()