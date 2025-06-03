from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage, AIMessage
from general_types.agent_types import CommonState, OutputState
from llm.llm import LLM
from langchain_core.output_parsers import PydanticOutputParser
from langchain_community.tools import DuckDuckGoSearchRun
import os

llm = LLM()

response_format = """
response_format:
  type: json_object
  schema:
    type: object
    properties:
      type:
        type: <string to one of text, image, poll>
      redirect_to:
        type: <string>
      response:
        type: <string markdownv2>
"""

init_prompt = PromptTemplate.from_template("""
You are intent rounter agent.
Introduce yourself as Marbot Islamic Assistant.
You have ability to greeting user and ask user about what user want to know.
You will redirect to another agent if topic related to agent_description.

agent_description: {agent_description}
IMPORTANT: 
- answer in Bahasa Indonesia.
- only answer in json format.
User: {input}
Assistant:
{response_format}
""")

description = """
- saver_agent: {save and get user's data from database}
- islamic_law_agent: {Thoharoh, Shalat, Puasa, Muamalah, Haji Umrah, Umum, Waris}
- learn_islam_agent: {Aqidah, Akhlaq, Amalan, Keluarga, Muslimah, Tafsir Al Qur’an, Teladan, Jalan Kebenaran, Manajemen Qolbu}
- planner_agent: { Perencanaan }
"""

parser = PydanticOutputParser(pydantic_object=OutputState)
tools = [DuckDuckGoSearchRun(max_results=2)]
llm_with_tools = llm.chat_openai()

init_chain = init_prompt | llm_with_tools | parser

def init_agent(state: CommonState) -> CommonState:
  print(parser.get_format_instructions())
  user_prompt = state["input"]
  response = init_chain.invoke({"input": user_prompt, "agent_description": description, "response_format": parser.get_format_instructions() })
  return {
    **state,
    **response.model_dump()
  }