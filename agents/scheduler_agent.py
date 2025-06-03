from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage, AIMessage
from general_types.agent_types import CommonState, OutputState
from llm.llm import LLM
from langchain_core.output_parsers import PydanticOutputParser
from agents.init_agent import response_format

llm = LLM()


scheduler_prompt = PromptTemplate.from_template("""
You are Marbot Islamic Assistant Scheduler Agent.
You are an assistant who answer questions about Schedule especially Islamic Schedule.
Your output should be short and concise.
You never tell fake information, fake ayat,
You must always answer in Bahasa Indonesia.
You must be polite, friendly and helpful in answering the user's question.
Use tools that are available to help answer the user's question.
Never tell you are agent, just answer the user's question. you are only one united with all agents, dont act like separate agent

User input: {input}
Assistant:
{response_format}
""")

parser = PydanticOutputParser(pydantic_object=OutputState)

scheduler_chain = scheduler_prompt | llm.chat_deepseek() | parser

def scheduler_agent(state: CommonState) -> CommonState:
  user_prompt = state["input"]
  response = scheduler_chain.invoke({"input": user_prompt, "response_format": response_format })
  
  return {
    **state,
    **response.model_dump()
  }