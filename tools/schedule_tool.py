from pydantic import BaseModel, Field
from langchain_core.tools import tool
from apscheduler.schedulers.background import BackgroundScheduler
import dateparser
from datetime import datetime
from config.settings import Settings

# Initialize scheduler
scheduler = BackgroundScheduler()
scheduler.start()

# --- Step 1: Define what happens when the event is triggered
from telegram import Bot

settings = Settings()
bot = Bot(token=settings.telegram.telegram_token)

def execute_event(event: str, user_id: str):
    message = f"🔔 Reminder: '{event}' is happening now!"
    print(message)
    chat_id = user_registry.get(user_id)
    print(chat_id)
    if chat_id:
        try:
            bot.send_message(chat_id=chat_id, text=message)
        except Exception as e:
            print(f"❌ Failed to send to chat_id {chat_id}: {e}")
    else:
        print(f"❌ User {user_id} not found in registry.")

# --- Step 2: LangChain Tool Schema
class ScheduleInput(BaseModel):
    event: str = Field(..., description="Name of the event (e.g., 'meeting', 'prayer')")
    time_info: str = Field(..., description="Time information, e.g., 'next Friday at 8PM' or '2025 06 01 14:00'")

# --- Step 3: LangChain Tool Function
@tool
def create_schedule(input: ScheduleInput) -> str:
    """
    Schedule an event at a given natural time.
    Example: event='Weekly Sync', time_info='Friday at 9PM'
    """
    dt = dateparser.parse(input.time_info, languages=["id", "en"])
    if not dt:
        return f"❌ Failed to parse time: '{input.time_info}'"

    # Add to scheduler
    scheduler.add_job(
        execute_event,
        'date',
        run_date=dt,
        args=[input.event],
        id=f"{input.event}-{dt.isoformat()}",
        replace_existing=True
    )

    return f"✅ Event '{input.event}' scheduled on {dt.strftime('%A, %d %B %Y at %H:%M')}."