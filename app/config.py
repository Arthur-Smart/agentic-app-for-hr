from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # AWS configuration
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    aws_region: str = ""
    s3_bucket_name: str = ""

    # Bedrock model configuration
    bedrock_embed_model: str = ""
    bedrock_chat_model: str = ""
    embed_dim: int = 0

    max_upload_bytes:int=10485760  # 10 MB

    # Pinecone configuration
    pinecone_api_key: str = ""
    pinecone_index_name: str = ""
    pinecone_cloud: str = ""
    pinecone_region: str = ""
    pinecone_ready_timeout: int = 0

    # PostgreSQL configuration
    database_url: str = ""

    # RIUS Observability configuration
    rius_api_key: str = ""
    rius_service_name: str = ""
    rius_disable: bool = False
    rius_capture_content: bool = False

    min_relevance:float=0.25
    hitl_enabled:bool=True
    memory_turns:int=6


@lru_cache
def settings() -> Settings:
    return Settings()