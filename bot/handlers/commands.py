from telegram import Update
from telegram.ext import ContextTypes

from templates.templates import WELCOME_MESSAGE


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_chat.send_message(text=WELCOME_MESSAGE)
