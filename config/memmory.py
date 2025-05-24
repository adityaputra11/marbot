from langgraph.checkpoint.postgres import PostgresSaver
from config.settings import Settings

settings = Settings()
DB_URI = settings.database.db_url

with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
 checkpointer.setup()
 
 