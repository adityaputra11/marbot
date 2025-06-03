from typing import Optional
from dataclasses import dataclass


@dataclass
class TelegramConfigType:
    telegram_token: str


@dataclass
class WhatsappConfigType:
    access_token: str
    phone_number_id: str

@dataclass
class AIConfigType:
    # open_api_key: Optional
    deepseek_api_key: Optional
    gemini_api_key: Optional
    perplexity_api_key: Optional
    together_api_key: Optional
    litellm_api_key: Optional
    litellm_api_base: Optional


@dataclass
class AppConfigType:
    env: str
    debug: bool

@dataclass
class DatabaseConfigType:
    db_url: str
    second_db_url: str
    
@dataclass
class VectorStoreConfigType:
    vectorstore_path: str
    user_agent: str