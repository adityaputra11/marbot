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

class OutputState(BaseModel):
    type: str = Field(..., description="between text, image, poll")
    response: str = Field(..., description="The response to the user, use markdownv2 telegram format")
    redirect_to: str = Field(..., description="Redirect to the next agent if empty then END")
        
