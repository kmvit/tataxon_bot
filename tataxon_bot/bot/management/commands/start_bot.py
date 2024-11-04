import logging
from telegram import ReplyKeyboardMarkup, Update, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes, filters, MessageHandler
)

from django.core.management.base import BaseCommand
from django.conf import settings
from asgiref.sync import sync_to_async

from api.models import Category

CATEGORIES = ['Обучение', 'Ремонт техники', 'Оборудование']
INFO_MESSAGE = 'Запускает Telegram-бота.'
WELCOME_MESSAGE = (
    'Привет, {name}! Это бот с объявлениями сайта TATAXON.UZ!'
    'Нажми на кнопку "categories", если нужны объявления'
)
IN_FRONT_OF_THE_BUTTONS = 'Выберите интересующую категорию.'



logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def presentation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обрабатывает команду (кнопку) /start, текстовое сообщение и 
    отправляет информационное сообщение с выбором действий.
    """
    chat = update.effective_chat
    name = update.message.chat.first_name
    buttons = ReplyKeyboardMarkup([['/categories'], ['Выход']])
    await context.bot.send_message(
        chat_id=chat.id,
        text=WELCOME_MESSAGE.format(name=name),
        # Добавим кнопки в содержимое отправляемого сообщения
        reply_markup=buttons
    )


@sync_to_async
def get_categories():
    """
    Получение всех категорий из объявлений в список.
    """
    sql = Category.objects.values()
    x = [category['title'] for category in sql]
    #print(x)
    return x


async def categories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обрабатывает команду (кнопку) /categories и выводит кнопки c категориями.
    """
    chat = update.effective_chat
    name = update.message.chat.first_name
    # Вот она, наша кнопка.
    # Обратите внимание: в класс передаётся список, вложенный в список, 
    # даже если кнопка всего одна.
    cats = await get_categories()
    
    button = ReplyKeyboardMarkup([[cat for cat in cats]])
    await context.bot.send_message(
        chat_id=chat.id,
        #text=IN_FRONT_OF_THE_BUTTONS,
        
        text='проверка',
        # Добавим кнопку в содержимое отправляемого сообщения
        reply_markup=button
        )


class Command(BaseCommand):
    help = INFO_MESSAGE

    def handle(self, *args, **kwargs):
        """Создает приложение Телеграм-бота."""
        application = (
            ApplicationBuilder()
            .token(settings.TELEGRAM_TOKEN)
            .build()
        )

        application.add_handler(CommandHandler("start", presentation))
        application.add_handler(CommandHandler("categories", categories))
        
        #application.add_handler(MessageHandler(filters.TEXT, presentation))
        

        application.run_polling(allowed_updates=Update.ALL_TYPES)
