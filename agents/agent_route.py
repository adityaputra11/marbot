from langgraph.graph import END

base_agent_list = [
    "init_agent", "islamic_law_agent", "learn_islam_agent", "scheduler_agent", "saver_agent"
]

agent_mapping = {
    "init_agent": base_agent_list
}

def get_agent_list(current_agent: str) -> list[str]:
    return agent_mapping.get(current_agent, [])