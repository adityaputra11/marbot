from langgraph.graph import END

base_agent_list = [
    "init_agent", "arab_agent", "fiqh_agent", "history_agent",
    "quran_agent", "scheduler_agent", "tafsir_agent", "tassawuf_agent", "tauhid_agent",
]

# 1. Manual agent redirection map (bukan pakai tag similarity)
agent_mapping = {
    "init_agent": base_agent_list,
    "fiqh_agent": ["tafsir_agent"],
    "arab_agent": [],
    "tafsir_agent": ["quran_agent","arab_agent"],
    "tassawuf_agent": [],
    "tauhid_agent": ["quran_agent", "tafsir_agent"],
    "quran_agent": ["tafsir_agent","arab_agent"],
    "scheduler_agent": [],
    "history_agent": [],
}

# 2. Fungsi untuk LLM prompt injection
def get_agent_list(current_agent: str) -> list[str]:
    return agent_mapping.get(current_agent, [])

# 3. Routing map untuk LangGraph (di create_agent_graph)
def get_routing_map_for_langgraph(agent: str) -> dict:
    targets = agent_mapping.get(agent, [])
    routing = {t: t for t in targets}
    routing["END"] = END
    return routing