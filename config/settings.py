import getpass
import os
from dotenv import load_dotenv
from general_types.genera_types import TelegramConfigType, AIConfigType, AppConfigType


class Settings:
    telegram: TelegramConfigType
    ai: AIConfigType
    app: AppConfigType

    def __init__(self):
        load_dotenv()
        self.telegram = TelegramConfigType(
            telegram_token=os.getenv("TELEGRAM_TOKEN")
        )

        self.ai = AIConfigType(
            deepseek_api_key=os.getenv("DEEPSEEK_API_KEY"),
            open_api_key=os.getenv("OPEN_API_KEY"),
            gemini_api_key=os.getenv("GEMINI_API_KEY")
        )

        self.app = AppConfigType(
            env=os.getenv("ENV", "development"),
            debug=os.getenv("DEBUG", "false").lower() == "true",
        )
