
from telegram import Poll, Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand 
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
from telegram.constants import ChatAction
from config.settings import Settings
from core.runner import run_agent_response_with_agent
from services.auth.AuthService import AuthService
import asyncio

settings = Settings()
auth_service = AuthService()


async def registerOrLogin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    username = update.message.from_user.username
    name = update.message.from_user.name
    
    print(f"username: {username}")
    print(f"name: {name}")
    result = await auth_service.register(username, name)
    print(f"result: {result}")  
    if result['status']:
        await update.message.reply_text(f'Assalamualaikum {update.effective_user.first_name}')
    else:
        await update.message.reply_text(f'{result["message"]}')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    chat_id = update.effective_chat.id

    sent_message = await context.bot.send_message(chat_id=chat_id, text="Marbot lagi memproses...")
    await update.message.chat.send_action(action=ChatAction.TYPING)

    response_task = asyncio.create_task(
        run_agent_response_with_agent(text, session_id=update.effective_user.id, user_name=update.effective_user.first_name)
    )
    async def send_loading_hint():
        await asyncio.sleep(5) 
        if not response_task.done():
            await context.bot.send_message(chat_id=chat_id, text="Bentar dikit ya... masih nyari jawaban terbaik")
    loading_hint_task = asyncio.create_task(send_loading_hint())
    response = await response_task

    if not loading_hint_task.done():
        loading_hint_task.cancel()

    await context.bot.delete_message(chat_id=chat_id, message_id=sent_message.message_id)
    await update.message.reply_markdown_v2(response)

async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.username
    result = await auth_service.subscribe(username)   
    if result['status']:
        await update.message.reply_text(f'Berhasil berlangganan')
    else:
        await update.message.reply_text(f'{result["message"]}')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("Akhlak", callback_data='akhlak'),
            InlineKeyboardButton("Fiqih", callback_data='fiqih'),
            InlineKeyboardButton("Tauhid", callback_data='tauhid'),
        ],
        [
            InlineKeyboardButton("Hadis", callback_data='hadis'),
            InlineKeyboardButton("Tafsir", callback_data='tafsir'),
            InlineKeyboardButton("Sejarah Islam", callback_data='sejarah_islam'),
        ],
        [
            InlineKeyboardButton("Premium", callback_data='premium'),
            InlineKeyboardButton("Tentang Marbot", callback_data='about'),
            InlineKeyboardButton("Info Hari Ini", callback_data='today'),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Assalamualaikum! Pilih topik belajar Islam yang ingin kamu dalami:",
        reply_markup=reply_markup
    )
    

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Acknowledge callback to remove loading animation
    data = query.data
    message = """
            🤖 *Marbot* - Your All-in-One AI Assistant

            ✨ *GRATIS | MINGGUAN*
            ☑️ 50 permintaan teks
            ☑️ GPT-4.1 mini & GPT-4o mini
            ☑️ DeepSeek-V3 & Gemini 2.5 Flash
            ☑️ Pencarian web dengan Perplexity
            ☑️ GPT-4o untuk gambar

            🌟 *PREMIUM | BULANAN*
            ✅ 100 permintaan teks per hari
            ✅ Semua fitur Gratis +
            ✅ Voice query dan respon suara
            ✅ 10 gambar Midjourney & Flux
            Harga: ⭐ 200*


            Untuk info lebih lanjut, ketik /subscribe atau hubungi admin.
            """
    if(data =="premium"):
        await query.edit_message_text(text=message)
        return
    await query.edit_message_text(text=f"Kamu memilih: {data}")

async def post_init(application):
    commands = [
        BotCommand("help", "Get support if you're stuck"),
        BotCommand("group", "Add Copilot into Group"),
        BotCommand("newchat", "Start new chat"),
    ]
    await application.bot.set_my_commands(commands)

async def handle_message2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    
    # Kirim pesan pertama
    sent_message = await context.bot.send_message(chat_id=chat_id, text="Sedang memproses...")
    
    # Simulasi delay
    await asyncio.sleep(2)
    
    # Hapus pesan lama
    await context.bot.delete_message(chat_id=chat_id, message_id=sent_message.message_id)
    
    # Kirim pesan baru
    sent_message = await context.bot.send_message(chat_id=chat_id, text="Ini hasil akhirnya!")
    
    # Jika mau lanjut animasi lagi, ulangi hapus & kirim pesan baru
def run_telegram_bot():
    app = ApplicationBuilder().token(settings.telegram.telegram_token).post_init(post_init).build()

    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, handle_message))

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("subscribe", subscribe))
    app.add_handler(CallbackQueryHandler(button_callback))      
    app.run_polling()
