# marbot/core/runner.py
from langchain_deepseek import ChatDeepSeek
from langchain.schema import HumanMessage, SystemMessage
from config.settings import Settings
from tools.schedule_tool import create_schedule
import telegramify_markdown
from langchain_core.messages import BaseMessage, AIMessage
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from pydantic import BaseModel, Field


settings = Settings()

llm = ChatDeepSeek(
    model="deepseek-chat",  # bisa diganti deepseek, gemini, dll
    temperature=0,
    api_key=settings.ai.deepseek_api_key,
    max_tokens=1000,
)
prompt = ChatPromptTemplate.from_messages([
    SystemMessage(
        content="""You are a kind and wise Islamic teacher (ustadz) who answers questions with patience and humility.
                  Always reply in Bahasa Indonesia no matter what language the user uses.
                  Your tone is soft, peaceful, and respectful. Base your answers on Islamic teachings and everyday life values.
                  Please be concise and go straight to the point when you answer.
                  """),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}"),  # Cannot use HumanMessaeg
])


store = {}


def get_by_session_id(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


tools = [create_schedule]
llm_with_tools = llm.bind_tools(tools)
chain = prompt | llm_with_tools
chain_with_history = RunnableWithMessageHistory(
    chain,
    # Uses the get_by_session_id function defined in the example
    # above.
    get_by_session_id,
    input_messages_key="question",
    history_messages_key="history",
)


async def run_agent_response(prompt: str, session_id: str) -> str:
    try:
        response = await chain_with_history.ainvoke({"question": prompt}, config={"configurable": {"session_id": session_id}},)
        return telegramify_markdown.markdownify(response.content)
    except Exception as e:
        return f"❌ Error: {e}"
