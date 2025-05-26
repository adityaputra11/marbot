from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage, AIMessage
from general_types.agent_types import CommonState, OutputState
from llm.llm import LLM
from langchain_core.output_parsers import JsonOutputParser
from agents.agent_route import get_agent_list

llm = LLM()

quran_prompt = PromptTemplate.from_template("""
You are Marbot Islamic Assistant Quran Agent.
You are an assistant who answer questions about Quran.
Your output should be short and concise.
You never tell fake information, fake ayat,
Never tell you are agent, just answer the user's question. you are only one united with all agents, dont act like separate agent

MessageBefore: {messages}

User: {input}
Assistant:
redirect_to: one of related agents {agent_list}
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

parser = JsonOutputParser(pydantic_object=OutputState)

quran_chain = quran_prompt | llm.chat_deepseek() | parser

def quran_agent(state: CommonState) -> CommonState:
  user_prompt = state["input"]
  response = quran_chain.invoke({"input": user_prompt, "agent_list": get_agent_list("quran_agent"), "messages": state.get("messages", []) })
  
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