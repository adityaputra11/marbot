from langgraph.prebuilt.chat_agent_executor import AgentState
from langgraph.graph import StateGraph
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
from pydantic import BaseModel, Field   

class CustomState(AgentState):
    user_name: str
    context: str
    
class CommonState(TypedDict):
    user_name: str
    input: str
    messages: list[BaseMessage]
    
class OutputState(BaseModel):
    user_name: str = Field(..., description="The user name")
    input: str = Field(..., description="The input to the agent")
    messages: list[BaseMessage] = Field(..., description="The messages to the user")
    response: str = Field(..., description="The response to the user")
    next_agent: str = Field(..., description="Redirect to the next agent")
    done: bool = Field(..., description="If the agent is done, only True or False")