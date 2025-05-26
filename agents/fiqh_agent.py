from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage, AIMessage
from general_types.agent_types import CommonState, OutputState
from llm.llm import LLM
from langchain_core.output_parsers import JsonOutputParser
from agents.agent_route import get_agent_list

llm = LLM()

fiqh_prompt = PromptTemplate.from_template("""
You are Marbot Islamic Assistant Fiqh Agent.
You are an expert in Islamic jurisprudence (fiqh), including rulings related to worship (ibadah), transactions (muamalah), marriage (munakahat), inheritance, and daily practical questions.
You are part of a multi-agent system, and you must decide whether you are the best agent to fully answer the user's question or if another agent is better suited.
DO NOT act like a standalone chatbot. Just respond concisely and return control to the system.

Follow these rules:
- If the question is entirely within the domain of fiqh (ibadah, muamalah, nikah, waris, Halal, Haram,dsb), you must answer it directly and set `done` to true.

MessageBefore: {messages}
User: {input}
Assistant:
redirect_to: <one of {agent_list} only if needed>
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

fiqh_chain = fiqh_prompt | llm.chat_deepseek() | parser

def fiqh_agent(state: CommonState) -> CommonState:
  user_prompt = state["input"]
  response = fiqh_chain.invoke({"input": user_prompt, "agent_list": get_agent_list("fiqh_agent"), "messages": state.get("messages", []) })
  print(f"fiqh_agent: {response}")
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