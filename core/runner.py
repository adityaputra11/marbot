# marbot/core/runner.py
from langchain_deepseek import ChatDeepSeek
from langchain.schema import HumanMessage, SystemMessage
from langchain_core.messages import BaseMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.prebuilt import create_react_agent
from config.settings import Settings
from tools.schedule_tool import create_schedule
import telegramify_markdown
import psycopg2

settings = Settings()

llm = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0,
    api_key=settings.ai.deepseek_api_key,
    max_tokens=1000,
)

# Perbaikan 1: Gunakan SystemMessage dengan format yang benar
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a kind and wise Islamic teacher (ustadz) who answers questions with patience and humility.
                  Always reply in Bahasa Indonesia no matter what language the user uses.
                  Your tone is soft, peaceful, and respectful. Base your answers on Islamic teachings and everyday life values.
                  Use the tools provided to you to answer the user's question.
                  Please be concise and go straight to the point when you answer."""),
    MessagesPlaceholder(variable_name="messages"),
])

tools = [create_schedule]

# Perbaikan 2: Inisialisasi PostgresSaver dengan benar
DB_URI = settings.database.db_url

# Global variable untuk menyimpan checkpointer
checkpointer = None
agent = None


def initialize_agent():
    """Initialize agent dengan error handling yang proper"""
    global checkpointer, agent
    
    try:
        # Coba gunakan PostgreSQL checkpointer
        checkpointer = PostgresSaver.from_conn_string(DB_URI).__enter__()
        checkpointer.setup()
        agent = create_react_agent(
                model=llm,
                tools=tools,
                prompt=prompt,
                checkpointer=checkpointer,
            )
        print("✅ Agent initialized with PostgreSQL checkpointer")
        return True
        
    except Exception as e:
        print(f"⚠️ PostgreSQL checkpointer failed: {e}")
        
        try:
            # Fallback ke MemorySaver
            from langgraph.checkpoint.memory import MemorySaver
            checkpointer = MemorySaver()
            
            agent = create_react_agent(
                model=llm,
                tools=tools,
                prompt=prompt,
                checkpointer=checkpointer,
            )
            print("✅ Agent initialized with memory checkpointer")
            return True
            
        except Exception as fallback_error:
            print(f"⚠️ Memory checkpointer failed: {fallback_error}")
            
            try:
                # Last resort: tanpa checkpointer
                agent = create_react_agent(
                    model=llm,
                    tools=tools,
                    prompt=prompt,
                )
                print("✅ Agent initialized without checkpointer (no conversation history)")
                checkpointer = None
                return True
                
            except Exception as final_error:
                print(f"❌ Failed to initialize agent: {final_error}")
                return False

# Initialize agent saat module dimuat
if not initialize_agent():
    raise RuntimeError("Failed to initialize agent")

async def run_agent_response(user_prompt: str, session_id: str) -> str:
    """
    Menjalankan agent dan mengembalikan response
    
    Args:
        user_prompt: Pesan dari user
        session_id: ID sesi untuk tracking conversation
    
    Returns:
        String response yang sudah diformat untuk Telegram
    """
    try:
        # Perbaikan 4: Pastikan config yang benar
        config = {"configurable": {"thread_id": session_id}}
        
        # Perbaikan 5: Format input yang benar untuk agent
        response = await agent.ainvoke(
            {"messages": [HumanMessage(content=user_prompt)]}, 
            config=config
        )
        
        # Perbaikan 6: Extract AI message dengan lebih robust
        messages = response.get("messages", [])
        
        # Cari AI message terakhir
        ai_message = None
        for msg in reversed(messages):
            if isinstance(msg, AIMessage):
                ai_message = msg
                break
        
        if ai_message and ai_message.content:
            # Format untuk Telegram
            formatted_response = telegramify_markdown.markdownify(ai_message.content)
            return formatted_response
        else:
            return "❌ Maaf, tidak ada respon dari sistem."
            
    except Exception as e:
        error_msg = f"❌ Terjadi kesalahan: {str(e)}"
        print(f"Error in run_agent_response: {e}")
        return telegramify_markdown.markdownify(error_msg)

# Perbaikan 7: Tambahkan fungsi untuk cleanup jika diperlukan
def cleanup():
    """Cleanup resources"""
    global checkpointer
    try:
        if checkpointer and hasattr(checkpointer, '__exit__'):
            checkpointer.__exit__(None, None, None)
    except Exception as e:
        print(f"Error during cleanup: {e}")

# Tambahkan ini jika ingin auto-cleanup saat program selesai
import atexit
atexit.register(cleanup)