from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from telegram.constants import ChatAction
from config.settings import Settings
from core.chat_registry import user_registry
from core.runner import run_agent_response

settings = Settings()


async def greeting(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'waalaikumasalam {update.effective_user.first_name}')


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_registry[str(update.effective_user.id)] = update.effective_chat.id
    text = update.message.text
    await update.message.chat.send_action(action=ChatAction.TYPING)
    response = await run_agent_response(text, session_id=update.effective_user.id)
    await update.message.reply_text(response, parse_mode="MarkdownV2")


def run_telegram_bot():
    app = ApplicationBuilder().token(settings.telegram.telegram_token).build()
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CommandHandler("start", greeting))
    app.run_polling()
