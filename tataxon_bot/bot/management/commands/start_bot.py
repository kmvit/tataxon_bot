import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from django.core.management.base import BaseCommand
from django.conf import settings

INFO_MESSAGE = 'Запускает Telegram-бота.'
WELCOME_MESSAGE = 'Привет! Это tataxon бот!'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает команду /start и отправляет приветственное сообщение."""
    await update.effective_chat.send_message(text=WELCOME_MESSAGE)


class Command(BaseCommand):
    help = INFO_MESSAGE

    def handle(self, *args, **kwargs):
        """Создает приложение Телеграм-бота."""
        application = (
            ApplicationBuilder()
            .token(settings.TELEGRAM_TOKEN)
            .build()
        )

        application.add_handler(CommandHandler("start", start))

        application.run_polling(allowed_updates=Update.ALL_TYPES)
