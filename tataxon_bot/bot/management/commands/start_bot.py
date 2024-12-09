import logging
import os

from asgiref.sync import sync_to_async
from django.conf import settings
from django.core.management.base import BaseCommand
from dotenv import load_dotenv
from telegram import (BotCommand, InlineKeyboardButton, InlineKeyboardMarkup,
                      ReplyKeyboardRemove, Update)
from telegram.ext import (ApplicationBuilder, CallbackContext,
                          CallbackQueryHandler, CommandHandler, ContextTypes,
                          MessageHandler, filters)

from api.models import Advertisement, Category

INFO_MESSAGE = 'Запускает Telegram-бота.'
WELCOME_MESSAGE = 'Привет! Это tataxon бот!'
NO_AD_MESSAGE = 'Нет доступных объявлений на данный момент.'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: CallbackContext):
    """
    Обрабатывает команду /start
    и отправляет приветственное сообщение с кнопками.
    """
    reply_markup = ReplyKeyboardRemove()
    await update.message.reply_text(
        text=WELCOME_MESSAGE,
        reply_markup=reply_markup
    )


@sync_to_async
def get_latest_ad():
    """
    Функция для получения последнего объявления из базы данных.
    Работает в синхронном контексте и возвращает
    последний объект Advertisement.
    """
    return Advertisement.objects.latest('pub_date')


async def send_ad(update, context):
    """
    Обрабатывает команду /ad
    и отправляет объявление с изображением.
    """
    try:
        ad = await sync_to_async(Advertisement.objects.latest)('pub_date')
        await update.message.reply_text(
            f"Новое объявление:\n\n*{ad.title}*\n{ad.short_description}\n[Ссылка на объявление]({ad.full_url})",
            parse_mode="Markdown",
        )
        if ad.image:
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


@sync_to_async
def get_categories():
    """Получает список категорий из базы данных."""
    return list(Category.objects.all())


@sync_to_async
def get_ads_by_category(category_id):
    """Получает объявления по ID категории."""
    return list(Advertisement.objects.filter(category_id=category_id))


async def show_categories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отображает список категорий с кнопками."""
    categories = await get_categories()
    if not categories:
        await update.message.reply_text("Категорий пока нет.")
        return

    keyboard = [
        [InlineKeyboardButton(
            category.title, callback_data=f"category_{category.id}")]
        for category in categories
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Выберите категорию:", reply_markup=reply_markup)


async def handle_category_selection(
        update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает выбор категории и выводит объявления из неё."""
    query = update.callback_query
    await query.answer()
    category_id = query.data.split("_")[1]
    ads = await get_ads_by_category(category_id)

    if not ads:
        await query.edit_message_text("Объявлений в этой категории пока нет.")
        return

    response = "\n\n".join(
        f"*{ad.title}*\n{ad.short_description}\n[Ссылка на объявление]({ad.full_url})"
        for ad in ads
    )
    await query.edit_message_text(
        text=response,
        parse_mode="Markdown",
    )


class Command(BaseCommand):
    help = INFO_MESSAGE

    def handle(self, *args, **kwargs):
        """Создаёт приложение Телеграм-бота."""
        load_dotenv()
        application = (
            ApplicationBuilder()
            .token(os.environ.get("TELEGRAM_TOKEN"))
            .build()
        )
        # Устанавливаем команды для бота
        commands = [
            BotCommand("start", "Главное меню"),
            BotCommand("ad", "Последнее объявление"),
            BotCommand("categories", "Показать категории"),
        ]
        # Регистрируем команды
        application.bot.set_my_commands(commands)
        # Добавляем обработчики
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.Text("/ad"), send_ad))
        application.add_handler(
            MessageHandler(filters.Text("/categories"), show_categories))
        application.add_handler(
            CallbackQueryHandler(
                handle_category_selection, pattern="^category_"))
        application.run_polling(allowed_updates=Update.ALL_TYPES)
