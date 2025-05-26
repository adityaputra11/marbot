from langgraph.graph import StateGraph, END, START
from general_types.agent_types import CommonState, OutputState
from agents.scheduler_agent import scheduler_agent
from agents.arab_agent import arab_agent
from agents.fiqh_agent import fiqh_agent
from agents.tafsir_agent import tafsir_agent
from agents.tassawuf_agent import tassawuf_agent
from agents.tauhid_agent import tauhid_agent
from agents.quran_agent import quran_agent
from agents.history_agent import history_agent
from agents.init_agent import init_agent
from langgraph.checkpoint.memory import MemorySaver
from agents.agent_route import base_agent_list, get_routing_map_for_langgraph

def log_and_return_next_agent(state):
    print(f"all state: {state}")
    if state["done"] is True:
        return "END"
    return state["next_agent"]


def create_agent_graph():
    builder = StateGraph(input=CommonState, output=OutputState)
    builder.add_node("init_agent", init_agent)
    builder.add_node("arab_agent", arab_agent)
    builder.add_node("fiqh_agent", fiqh_agent)
    builder.add_node("scheduler_agent", scheduler_agent)
    builder.add_node("tafsir_agent", tafsir_agent)
    builder.add_node("tassawuf_agent", tassawuf_agent)
    builder.add_node("tauhid_agent", tauhid_agent)
    builder.add_node("quran_agent", quran_agent)
    builder.add_node("history_agent", history_agent)
    for agent in base_agent_list:
        builder.add_conditional_edges(
        agent,
        log_and_return_next_agent,
        get_routing_map_for_langgraph(agent) 
        )
    
    builder.add_edge(START, "init_agent")
    checkpointer = MemorySaver()
    graph = builder.compile(checkpointer=checkpointer)
    return graph
