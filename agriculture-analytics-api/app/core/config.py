import os
from dotenv import load_dotenv
from pathlib import Path

# =========================
# Load .env safely (portable)
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent.parent
print("BASE_DIR =", BASE_DIR)
ENV_PATH = BASE_DIR / "env"

load_dotenv(ENV_PATH)


# =========================
# Settings Class (Clean + Safe)
# =========================
class Settings:
    DB_HOST: str = os.getenv("HOST", "localhost")
    DB_PORT: int = int(os.getenv("PORT", 3306))
    DB_USER: str = os.getenv("USER", "root")
    DB_PASSWORD: str = os.getenv("PASSWORD", "")
    DB_NAME: str = os.getenv("DB", "")

    def validate(self):
        missing = []

        if not self.DB_HOST:
            missing.append("HOST")
        if not self.DB_USER:
            missing.append("USER")
        if not self.DB_NAME:
            missing.append("DB")

        if missing:
            raise Exception(f"Missing environment variables: {missing}")


# create global settings instance
settings = Settings()
settings.validate()