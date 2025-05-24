import dateparser
from langchain_core.tools import tool


@tool
def create_schedule(event: str, time_info: str) -> str:
    """
    Add schedule base on natural response.
    Example time_info: 'malam Jumat jam 8'
    """
    dt = dateparser.parse(time_info, languages=["id", "en"])
    if not dt:
        return "❌ Gagal memahami waktu."
