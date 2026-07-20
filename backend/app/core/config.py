from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Bzorp"
    app_version: str = "0.1.0"
    env: str = "development"

    database_url: str = ""
    google_client_id: str = ""
    google_client_secret: str = ""
    telegram_bot_token: str = ""
    gemini_api_key: str = ""
    secret_key: str = ""

    frontend_url: str = "http://localhost:5173"
    backend_url: str = "http://localhost:8000"
    scheduler_time: str = "08:00"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
