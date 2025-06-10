from bot.telegram_bot import run_telegram_bot
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
from config.vdb import generate_from_file 

def main():
    # generate_from_file("data/rest-in-peace.txt","marbot_collection")
    run_telegram_bot()
    
    
if __name__ == "__main__":
    main()
