import asyncio
import logging

import aiogram
import aiogram.client.default

from .managers import config
from .managers import database
from .providers import environment
from .providers import guidance
from .providers import strings
from .telegram_bot import dispatcher as telegram_bot_dispatcher
from .telegram_bot.providers import buttons as telegram_bot_buttons
from .telegram_bot.providers import keyboards as telegram_bot_keyboards
from .telegram_bot.routers import callbacks as telegram_bot_callbacks
from .telegram_bot.routers import commands as telegram_bot_commands
from .telegram_bot.routers import messages as telegram_bot_messages
from .telegram_bot.services import logger as telegram_bot_logger


async def main() -> None:
    config_manager = config.ConfigManager()
    database_manager = database.DatabaseManager()
    environment_provider = environment.EnvironmentProvider()
    guidance_provider = guidance.GuidanceProvider()
    strings_provider = strings.StringsProvider()

    # region telegram_bot

    telegram_buttons_provider = telegram_bot_buttons.ButtonsProvider(
        strings_provider=strings_provider,
    )
    telegram_keyboards_provider = telegram_bot_keyboards.KeyboardsProvider(
        buttons_provider=telegram_buttons_provider,
    )
    telegram_logger_service = telegram_bot_logger.LoggerService(
        filename="telegram_bot",
        level=logging.INFO,
        file_handling=config_manager.settings.file_logging,
    )

    aiogram_bot = aiogram.Bot(
        token=environment_provider.TELEGRAM_BOT_TOKEN,
        default=aiogram.client.default.DefaultBotProperties(
            parse_mode=aiogram.enums.ParseMode.HTML,
        ),
    )

    aiogram_callbacks_router = telegram_bot_callbacks.CallbacksRouter(
        database_manager=database_manager,
        guidance_provider=guidance_provider,
        keyboards_provider=telegram_keyboards_provider,
        strings_provider=strings_provider,
        logger_service=telegram_logger_service,
        aiogram_bot=aiogram_bot,
    )
    aiogram_commands_router = telegram_bot_commands.CommandsRouter(
        config_manager=config_manager,
        database_manager=database_manager,
        keyboards_provider=telegram_keyboards_provider,
        strings_provider=strings_provider,
        logger_service=telegram_logger_service,
        aiogram_bot=aiogram_bot,
    )
    aiogram_messages_router = telegram_bot_messages.MessagesRouter(
        config_manager=config_manager,
        guidance_provider=guidance_provider,
        keyboards_provider=telegram_keyboards_provider,
        strings_provider=strings_provider,
        logger_service=telegram_logger_service,
        aiogram_bot=aiogram_bot,
    )

    aiogram_dispatcher = telegram_bot_dispatcher.AiogramDispatcher(
        config_manager=config_manager,
        logger_service=telegram_logger_service,
        aiogram_bot=aiogram_bot,
        routers=[
            aiogram_callbacks_router,
            aiogram_commands_router,
            aiogram_messages_router,
        ],
    )

    # endregion

    await aiogram_dispatcher.polling_coroutine()


if __name__ == "__main__":
    asyncio.run(main())
