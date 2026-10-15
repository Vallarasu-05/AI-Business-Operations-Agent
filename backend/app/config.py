from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(__file__).resolve().parents[2]  # project root


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=(str(ROOT / ".env"),), extra="ignore")

    app_env: str = "development"
    data_mode: str = "mock"  # mock | live_readonly | live_write
    llm_provider: str = "google"  # google | openai
    llm_api_key: str = ""
    llm_model: str = "gemini-2.5-flash"

    database_url: str = ""
    vector_backend: str = "memory"  # memory | qdrant
    vector_db_url: str = "http://localhost:6333"
    use_postgres_checkpointer: bool = False

    internal_domain: str = "mycompany.com"
    api_key: str = ""

    data_dir: str = str(ROOT / "data")
    output_dir: str = str(ROOT / "outputs")

    google_client_id: str = ""
    google_client_secret: str = ""
    google_sheet_id: str = ""
    google_token_file: str = str(ROOT / "token.json")

    hubspot_access_token: str = ""
    n8n_base_url: str = "http://localhost:5678"
    n8n_webhook_secret: str = "change_me"
    web_search_api_key: str = ""

    @property
    def is_mock(self) -> bool:
        return self.data_mode == "mock"


settings = Settings()
