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
from pydantic import BaseModel, Field


settings = Settings()

llm = ChatDeepSeek(
    model_name="deepseek-chat",  # bisa diganti deepseek, gemini, dll
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
    HumanMessage(content="{input}")
])


class InMemoryHistory(BaseChatMessageHistory):
    """In memory implementation of chat message history."""

    def __init__(self):
        self._messages: list[BaseMessage] = []

    @property
    def messages(self) -> list[BaseMessage]:
        return self._messages

    def add_message(self, message: BaseMessage) -> None:
        self._messages.append(message)

    def add_messages(self, messages: list[BaseMessage]) -> None:
        self._messages.extend(messages)

    def clear(self) -> None:
        self._messages = []


store = {}


def get_by_session_id(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryHistory()
    return store[session_id]


tools = [create_schedule]
llm_with_tools = llm.bind_tools(tools)
chain = prompt | llm_with_tools
chain_with_history = RunnableWithMessageHistory(
    chain,
    # Uses the get_by_session_id function defined in the example
    # above.
    get_by_session_id,
    input_messages_key="input",
    history_messages_key="history",
)


async def run_agent_response(prompt: str, session_id: str) -> str:
    try:
        history = get_by_session_id(session_id=session_id)
        # history.add_message(AIMessage(content="Assalamualaikum"))
        response = await chain_with_history.ainvoke({"input": prompt}, config={"configurable": {"session_id": session_id}})
        if not isinstance(response, AIMessage):
            response = AIMessage(content=response.content)

        # history.add_message(response)

        print("🧠 Chat history:")
        for m in history.messages:
            print(f"{type(m).__name__}: {m.content}")

        return telegramify_markdown.markdownify(response.content)
    except Exception as e:
        return f"❌ Error: {e}"
