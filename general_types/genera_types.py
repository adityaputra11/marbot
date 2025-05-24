from typing import Optional
from dataclasses import dataclass


@dataclass
class TelegramConfigType:
    telegram_token: str


@dataclass
class AIConfigType:
    open_api_key: Optional
    deepseek_api_key: Optional
    gemini_api_key: Optional


@dataclass
class AppConfigType:
    env: str
    debug: bool
