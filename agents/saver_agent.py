import os
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage, AIMessage
from general_types.agent_types import CommonState, OutputState
from llm.llm import LLM
from langchain_core.output_parsers import PydanticOutputParser
from agents.init_agent import response_format
from langchain_tavily import TavilySearch

llm = LLM()

saver_prompt = PromptTemplate.from_template("""
You are intent saver agent.
You have ability to save user's input to database.
For common topic, answer it by using tools.
- TavilySearch: for search information from internet

IMPORTANT: answer in Bahasa Indonesia.
User: {input}
Assistant:
{response_format}
""")

description = """
- islamic_law_agent: {Thoharoh, Shalat, Puasa, Muamalah, Haji Umrah, Umum, Waris}
- learn_islam_agent: {Aqidah, Akhlaq, Amalan, Keluarga, Muslimah, Tafsir Al Qur’an, Teladan, Jalan Kebenaran, Manajemen Qolbu}
"""

tool = TavilySearch(max_results=2, api_key=os.getenv("TAVILY_API_KEY"))
tools = [tool]
llm_with_tools = llm.chat_openai().bind_tools(tools)

parser = PydanticOutputParser(pydantic_object=OutputState)

saver_chain = saver_prompt | llm_with_tools | parser

def saver_agent(state: CommonState) -> CommonState:
  user_prompt = state["input"]
  response = saver_chain.invoke({"input": user_prompt, "response_format": response_format })
  return {
    **state,
    **response.model_dump()
  }