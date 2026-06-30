from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    groq_api_key: str
    tavily_api_key: str

    mongo_uri: str
    mongo_db_name: str

    chroma_persist_dir: str = "./chroma_data"
    relevance_threshold: float = 0.55

    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    cross_encoder_model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"

    llm_model: str = "llama3-8b-8192"

    class Config:
        env_file = ".env"


def get_settings():
    return Settings()