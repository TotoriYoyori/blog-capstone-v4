import os
from pathlib import Path
from dotenv import load_dotenv

# --------------- Environmental Variables
ROOT = Path(__file__).resolve().parent
envdir = ROOT / ".env"
if envdir.exists():
    load_dotenv()

# --------------- Configuration Master and Subclasses
class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    BLEACH_ALLOWED_TAGS = [
        "p", "br",
        "b", "i", "u", "em", "strong",
        "ul", "ol", "li",
    ]

    @staticmethod
    def init_app(app):
        pass


class DevConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    'development': DevConfig,
    'production': ProductionConfig,
    'default': DevConfig,
}