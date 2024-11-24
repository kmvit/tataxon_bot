import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from django.core.management.base import BaseCommand
from django.conf import settings
from api.models import Advertisement

from asgiref.sync import sync_to_async

from dotenv import load_dotenv
import os


INFO_MESSAGE = 'Запускает Telegram-бота.'
WELCOME_MESSAGE = 'Привет! Это tataxon бот!'
NO_AD_MESSAGE = 'Нет доступных объявлений на данный момент.'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает команду /start и отправляет приветственное сообщение."""
    await update.effective_chat.send_message(text=WELCOME_MESSAGE)


@sync_to_async
def get_latest_ad():
    """
    Функция для получения последнего объявления из базы данных.
    Работает в синхронном контексте и возвращает
    последний объект Advertisement.
    """
    return Advertisement.objects.latest('pud_date')


async def send_ad(update, context):
    """Обрабатывает команду /ad и отправляет объявление с изображением."""
    try:
        # Извлекаем самое свежее объявление из базы данных
        ad = await sync_to_async(Advertisement.objects.latest)('pud_date')

        # Отправляем текст объявления
        await update.message.reply_text(
            f"Новое объявление:\n\n*{ad.title}*\n{ad.short_description}\n[Ссылка на объявление]({ad.full_url})",
            parse_mode="Markdown",
            disable_web_page_preview=True
        )
        # Отправляем изображение, если оно есть
        if ad.image:
            # Получаем полный путь к файлу
            image_path = os.path.join(settings.MEDIA_ROOT, ad.image.name)

            with open(image_path, 'rb') as photo:
                await update.message.reply_photo(photo)
        else:
            await update.message.reply_text("Изображение отсутствует.")

    except Advertisement.DoesNotExist:
        await update.message.reply_text("Объявлений пока нет.")
    except Exception as e:
        logging.error(f"Ошибка при отправке объявления: {e}")
        await update.message.reply_text(
            "Произошла ошибка при обработке запроса.")


class Command(BaseCommand):
    help = INFO_MESSAGE

    def handle(self, *args, **kwargs):
        """Создает приложение Телеграм-бота."""
        load_dotenv()
        application = (
            ApplicationBuilder()
            .token(os.environ.get("TELEGRAM_TOKEN"))
            .build()
        )

        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("ad", send_ad))

        application.run_polling(allowed_updates=Update.ALL_TYPES)
