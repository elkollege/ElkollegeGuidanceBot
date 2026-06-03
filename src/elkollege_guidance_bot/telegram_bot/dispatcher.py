import aiogram
import aiogram.types

from .services import logger
from .. import constants
from ..managers import config


class AiogramDispatcher(aiogram.Dispatcher):
    _COMMANDS = [
        aiogram.types.BotCommand(
            command="/start",
            description="Пройти профориентацию",
        ),
        aiogram.types.BotCommand(
            command="/export",
            description="Экспортировать БД",
        ),
    ]

    def __init__(
            self,
            config_manager: config.ConfigManager,
            logger_service: logger.LoggerService,
            aiogram_bot: aiogram.Bot,
            routers: list[aiogram.Router],
    ) -> None:
        self._config = config_manager
        self._logger = logger_service
        self._bot = aiogram_bot

        super().__init__(
            name=self.__class__.__name__,
        )

        self.include_routers(*routers)

        self._logger.info(f"{self.name} initialized!")

    # region Helpers

    async def polling_coroutine(self) -> None:
        try:
            await self._bot.delete_webhook(
                drop_pending_updates=self._config.settings.skip_updates,
            )

            await self.start_polling(self._bot)
        except Exception as exception:
            self._logger.log_exception(exception)

    # endregion

    # region Handlers

    async def _startup_handler(self) -> None:
        await self._bot.set_my_commands(
            commands=self._COMMANDS,
            scope=aiogram.types.BotCommandScopeDefault(),
        )

        self._logger.info(f"{self.name} started!")

    async def _error_handler(self, event: aiogram.types.ErrorEvent) -> None:
        if type(event.exception) in constants.AIOGRAM_IGNORED_EXCEPTIONS:
            return

        self._logger.log_exception(event.exception)

    async def _shutdown_handler(self) -> None:
        self._logger.info(f"{self.name} terminated")

    # endregion
