from pydantic import BaseModel,Field
from langchain_core.tools import tool
import dateparser
import re

class ScheduleInput(BaseModel):
    event: str = Field(..., description="This is event name.")
    time_info: str = Field(..., description="This is time info, format should 'YYYY MM DD HH:MM' ")
   
@tool
def create_schedule(input: ScheduleInput) -> str:
    """
    Tambah jadwal berdasarkan input alami pengguna.
    parsing kedalam format waktu yg valid
    Contoh: 'acara rapat', 'malam Jumat jam 8'
    """
    dt = dateparser.parse(input.time_info, languages=["id", "en"])
    if not dt:
        return "❌ Gagal memahami waktu."
    return f"Jadwal '{input.event}' berhasil dibuat pada {dt.strftime('%A, %d %B %Y pukul %H:%M')}."

