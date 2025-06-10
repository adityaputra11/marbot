import os
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage, AIMessage
from langchain_tavily import TavilySearch
from config.vdb import hash_file, retrieval
from general_types.agent_types import CommonState, OutputState
from llm.llm import LLM
from langchain_core.output_parsers import PydanticOutputParser
from langchain_community.tools import BraveSearch
from agents.init_agent import response_format

llm = LLM()

islamic_law_prompt = PromptTemplate.from_template("""
You are Islamic Law Agent. part of Marbot Islamic Assistant.
You are master of Islamic Law.

IMPORTANT: 
- answer in Bahasa Indonesia
- if context not relevant dont mind it
- you should mention person resource
- use readable structure message with emoticon and text style and quote
- end with wallahu'alam
- if you not sure the answer, just say wallahu'alam
                                                  
User: {input} Context:{context}
Assistant:
{response_format}
""")

parser = PydanticOutputParser(pydantic_object=OutputState)


# research_tool = TavilySearch(max_results=2, api_key=os.getenv("TAVILY_API_KEY"))
search_tool = BraveSearch.from_api_key(api_key=os.getenv("BRAVE_API_KEY"), search_kwargs={"count": 3})
tools = [ search_tool]

islamic_law_chain = islamic_law_prompt | llm.chat_openai() | parser

collection_name = "marbot_collection"

def islamic_law_agent(state: CommonState) -> CommonState:

  user_prompt = state["input"]
  context =retrieval("marbot_collection", user_prompt)
  print(context)
  response = islamic_law_chain.invoke({"input": user_prompt,"context":context, "response_format": response_format })
  
  return {
    **state,
    **response.model_dump()
  }