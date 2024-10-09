from telegram import Update

from bot import create_bot_app


def main():
    #  configure_logging()

    app = create_bot_app()

    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
