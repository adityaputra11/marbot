from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage, AIMessage
from general_types.agent_types import CommonState, OutputState
from llm.llm import LLM
from langchain_core.output_parsers import JsonOutputParser
from agents.agent_route import get_agent_list

llm = LLM()



init_prompt = PromptTemplate.from_template("""
Your name is Marbot, the Islamic Assistant Router Agent call your self (Marbot not Asisten Router Islami.).
You will Greet user and ask about what user want to know.
You are the first agent that will be called.
Always answer in Bahasa Indonesia.
Always tell agent use Bahasa Indonesia.
Send Clear command to agent, dont send any other text.
You should ask for clarification if user's question is not clear.
If user ask first then it is clear you need to redirect to other agent.

{agent_description}
If user ask about your capbilities, summarize agent description only once and set done to True.

Only respond with:
redirect_to: <one of {agent_list} only if needed>
response: <short polite response to user confirming redirection>

MessageBefore: {messages}
User: {input}

Instructions:
- If you can answer directly and don't need another agent → set `done = True` and leave `redirect_to` empty.
- If you only greet, answer greetings, or receive light questions → set `done = True`.
- If you need another agent to answer → set `done = False` and fill `redirect_to` with the agent name.

response_format:
  type: json_object
  schema:
    type: object
    properties:
      redirect_to:
        type: string
      response:
        type: string
      done:
        type: boolean
""")

description = """
- scheduler_agent: {"jadwal sholat","reminder", "event"}
- fiqh_agent: {"ibadah", "muamalah", "nikah", "waris", "Halal", "Haram"}
- tafsir_agent: {"tafsir", "tafsir quran"}
- tauhid_agent: {"aqidah", "syahadat", "tuhan esa"}
- tasawuf_agent: {"tazkiyah", "akhlaq", "tazkiyah quran"}
- quran_agent: {"quran", "quran quran"}
- arab_agent: {"nahwu", "sharaf", "vocabulary", "nahwu quran"}
- history_agent: {"sejarah", "sirah nabawi", "sirah hadis"}
- islamic_law_agent: {"hudud", "maqashid", "negara", "konstitusi", "hukum"}
"""

parser = JsonOutputParser(pydantic_object=OutputState)

init_chain = init_prompt | llm.chat_openai() | parser

def init_agent(state: CommonState) -> CommonState:
  user_prompt = state["input"]
  response = init_chain.invoke({"input": user_prompt, "agent_list": get_agent_list("init_agent"), "messages": state.get("messages", []), "agent_description": description })
  return {
    **state,
    "messages": [
      HumanMessage(content=user_prompt),
      AIMessage(content=response["response"])
    ],
    "response": response["response"],
    "next_agent": response["redirect_to"],
    "done": response["done"]
  }