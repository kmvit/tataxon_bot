from typing import Optional

from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    Defaults,
)

from handlers.commands import start
from utils.configs import TOKEN


def create_bot_app(defaults: Optional[Defaults] = None) -> Application:
    app: Application = (
        ApplicationBuilder()
        .token(TOKEN)
        .defaults(defaults)
        .build()
    )
    app.add_handler(CommandHandler("start", start))

    return app
