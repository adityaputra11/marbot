from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage, AIMessage
from general_types.agent_types import CommonState, OutputState
from llm.llm import LLM
from langchain_core.output_parsers import PydanticOutputParser
from agents.init_agent import response_format

llm = LLM()

learn_islam_prompt = PromptTemplate.from_template("""
You are Learn Islam Agent. part of Marbot Islamic Assistant.
You are master of Learn Islam.

IMPORTANT: answer in Bahasa Indonesia.
User: {input}
Assistant:
{response_format}
""")

parser = PydanticOutputParser(pydantic_object=OutputState)

learn_islam_chain = learn_islam_prompt | llm.chat_openai() | parser

def learn_islam_agent(state: CommonState) -> CommonState:
  user_prompt = state["input"]
  response = learn_islam_chain.invoke({"input": user_prompt, "response_format": response_format })
  
  return {
    **state,
    **response.model_dump()
  }