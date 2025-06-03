# marbot/core/runner.py
import telegramify_markdown
from agents.agent_graph import create_agent_graph

async def run_agent_response_with_agent(user_prompt: str, session_id: str, user_name: str) -> str:
    """This function is for response with agent"""
    try:
        config = {"configurable": {"thread_id": "1"}}
        print(f"config: {config}")
        graph = create_agent_graph()
        response = graph.invoke({"input": user_prompt, "user_name": user_name}, config=config)
        print(f"response: {response}")
        return telegramify_markdown.markdownify(response["response"])
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error in run_agent_response_with_agent: {e}")
        return telegramify_markdown.markdownify("Maaf, saya tidak mengerti Wallahua'lam")
