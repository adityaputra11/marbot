import getpass
import os
from dotenv import load_dotenv
from general_types.general_types import TelegramConfigType, AIConfigType, AppConfigType,\
DatabaseConfigType, WhatsappConfigType, VectorStoreConfigType


class Settings:
    telegram: TelegramConfigType
    ai: AIConfigType
    app: AppConfigType
    database: DatabaseConfigType
    whatsapp: WhatsappConfigType
    vectorstore: VectorStoreConfigType

    def __init__(self):
        load_dotenv()
        self.telegram = TelegramConfigType(
            telegram_token=os.getenv("TELEGRAM_TOKEN")
        )

        self.ai = AIConfigType(
            deepseek_api_key=os.getenv("DEEPSEEK_API_KEY"),
            # open_api_key=os.getenv("OPEN_API_KEY"),
            gemini_api_key=os.getenv("GEMINI_API_KEY"),
            perplexity_api_key=os.getenv("PERPLEXITY_API_KEY"),
            together_api_key=os.getenv("TOGETHER_API_KEY"),
            litellm_api_key=os.getenv("LITELLM_API_KEY"),
            litellm_api_base=os.getenv("LITELLM_API_BASE")  
        )

        self.app = AppConfigType(
            env=os.getenv("ENV", "development"),
            debug=os.getenv("DEBUG", "false").lower() == "true",
        )
        
        self.database = DatabaseConfigType(
            db_url=os.getenv("POSTGRES_NEON_URL"),
            second_db_url=os.getenv("POSTGRES_SUPABASE_URL") 
        )

        self.whatsapp = WhatsappConfigType(
            access_token=os.getenv("WHATSAPP_ACCESS_TOKEN"),
            phone_number_id=os.getenv("WHATSAPP_PHONE_NUMBER_ID")
        )
    
        self.vectorstore = VectorStoreConfigType(
            vectorstore_path=os.getenv("VECTOR_STORE_PATH"),
            user_agent=os.getenv("USER_AGENT")
        )