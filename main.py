from bot.telegram_bot import run_telegram_bot
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
from ingest.local import create_vector_store,search_similar_docs    
import asyncio

def main():
    # create_vector_store()
  run_telegram_bot()
    
    
if __name__ == "__main__":
    main()
