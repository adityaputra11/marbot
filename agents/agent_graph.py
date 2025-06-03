from langgraph.graph import StateGraph, END, START
from general_types.agent_types import CommonState, OutputState
from agents.scheduler_agent import scheduler_agent
from agents.islamic_law_agent import islamic_law_agent
from agents.learn_islam_agent import learn_islam_agent    
from agents.planner_agent import planner_agent
from agents.saver_agent import saver_agent
from agents.init_agent import init_agent
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.postgres import PostgresSaver
from agents.agent_route import base_agent_list
from config.settings import Settings

def log_and_return_next_agent(state):   
    print(f"all state: {state}")
    if state["redirect_to"] == "":
        return "END"
    return state["redirect_to"]


settings = Settings()   
def create_agent_graph():
    with PostgresSaver.from_conn_string(settings.database.db_url) as checkpointer:
        checkpointer.setup()
        print("checkpointer", "FIRST")
        builder = StateGraph(input=CommonState, output=OutputState)
        builder.add_node("init_agent", init_agent)
        builder.add_node("islamic_law_agent", islamic_law_agent)
        builder.add_node("learn_islam_agent", learn_islam_agent)
        builder.add_node("scheduler_agent", scheduler_agent)
        builder.add_node("saver_agent", saver_agent)
        builder.add_node("planner_agent", planner_agent)
        for agent in base_agent_list:
            builder.add_conditional_edges(
            agent,
            log_and_return_next_agent,
            {
                "islamic_law_agent": "islamic_law_agent",
                "learn_islam_agent": "learn_islam_agent",
                "scheduler_agent": "scheduler_agent",
                "saver_agent": "saver_agent",
                "planner_agent":"planner_agent",
                "END": END
            }
            )
        
        builder.add_edge(START, "init_agent")
        cp = InMemorySaver()
        graph = builder.compile(checkpointer=cp)
        return graph
