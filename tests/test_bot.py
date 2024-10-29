from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from django.conf import settings
from telegram import Update
from telegram.ext import ContextTypes

from bot.management.commands.start_bot import Command, start


@pytest.mark.asyncio
async def test_start_command():
    """Тестирует команду /start."""

    # Создаем имитацию обновления и контекста
    mock_update = AsyncMock(spec=Update)
    mock_context = AsyncMock(spec=ContextTypes.DEFAULT_TYPE)

    # Имитация чата
    mock_chat = AsyncMock()
    mock_update.effective_chat = mock_chat

    # Выполняем команду /start
    await start(mock_update, mock_context)

    # Проверяем, что отправлено правильное сообщение
    mock_chat.send_message.assert_called_once_with(
        text='Привет! Это tataxon бот!')


@patch('bot.management.commands.start_bot.ApplicationBuilder')
@patch('bot.management.commands.start_bot.CommandHandler',
       new_callable=MagicMock)
def test_command_handle(mock_command_handler, mock_application_builder):
    """Тестирует создание приложения бота."""

    mock_app = MagicMock()
    (mock_application_builder.return_value.token.return_value.
     build).return_value = mock_app

    command = Command()
    command.handle()

    # Проверяем, что приложение было создано с правильным токеном
    mock_application_builder.assert_called_once()
    mock_application_builder.return_value.token.assert_called_once_with(
        settings.TELEGRAM_TOKEN)

    # Проверяем, что обработчик команды /start был добавлен
    mock_app.add_handler.assert_called_once_with(
        mock_command_handler.return_value)

    # Проверяем, что метод run_polling был вызван с правильными параметрами
    mock_app.run_polling.assert_called_once_with(
        allowed_updates=Update.ALL_TYPES)
