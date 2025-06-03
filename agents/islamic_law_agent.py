from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage, AIMessage
from general_types.agent_types import CommonState, OutputState
from llm.llm import LLM
from langchain_core.output_parsers import PydanticOutputParser
from agents.init_agent import response_format

llm = LLM()

islamic_law_prompt = PromptTemplate.from_template("""
You are Islamic Law Agent. part of Marbot Islamic Assistant.
You are master of Islamic Law.

IMPORTANT: answer in Bahasa Indonesia.
User: {input}
Assistant:
{response_format}
""")

parser = PydanticOutputParser(pydantic_object=OutputState)

islamic_law_chain = islamic_law_prompt | llm.chat_openai() | parser

def islamic_law_agent(state: CommonState) -> CommonState:
  user_prompt = state["input"]
  response = islamic_law_chain.invoke({"input": user_prompt, "response_format": response_format })
  
  return {
    **state,
    **response.model_dump()
  }