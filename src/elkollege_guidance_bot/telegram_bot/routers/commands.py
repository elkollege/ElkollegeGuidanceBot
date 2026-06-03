import datetime
import io
import typing

import aiogram
import aiogram.filters
import aiogram.fsm.context
import pandas

from ..providers import keyboards
from ..services import logger
from ...managers import config
from ...managers import database
from ...providers import strings


class CommandsRouter(aiogram.Router):
    def __init__(
            self,
            config_manager: config.ConfigManager,
            database_manager: database.DatabaseManager,
            keyboards_provider: keyboards.KeyboardsProvider,
            strings_provider: strings.StringsProvider,
            logger_service: logger.LoggerService,
            aiogram_bot: aiogram.Bot,
    ) -> None:
        self._config = config_manager
        self._database = database_manager
        self._keyboards = keyboards_provider
        self._strings = strings_provider
        self._logger = logger_service
        self._bot = aiogram_bot

        super().__init__(
            name=self.__class__.__name__,
        )

        self.message.outer_middleware.register(
            self._outer_middleware,
        )
        self.message.register(
            self._start_handler,
            aiogram.filters.CommandStart(),
        )
        self.message.register(
            self._export_handler,
            aiogram.filters.Command("export", "exp"),
        )
        self.message.register(
            self._logs_handler,
            aiogram.filters.Command("logs"),
        )

        self._logger.info(f"{self.name} initialized!")

    # region Middlewares

    async def _outer_middleware(
            self,
            handler: typing.Callable[
                [
                    aiogram.types.Message,
                    dict[str, typing.Any],
                ],
                typing.Awaitable[typing.Any],
            ],
            message: aiogram.types.Message,
            data: dict[str, typing.Any],
    ) -> typing.Any:
        if message.from_user is None or message.text is None:
            return None

        is_admin = message.from_user.id in self._config.settings.admins_list
        state = data["raw_state"]

        data["is_admin"] = is_admin

        if message.text.startswith("/"):
            self._logger.log_telegram_user_interaction(
                user=message.from_user,
                interaction=f"{message.text} ({is_admin=}, {state=})",
            )

        return await handler(message, data)

    # endregion

    # region Handlers

    async def _start_handler(
            self,
            message: aiogram.types.Message,
            state: aiogram.fsm.context.FSMContext,
    ) -> None:
        current_state = await state.get_state()

        if current_state is not None:
            await self._bot.send_message(
                chat_id=message.chat.id,
                text=self._strings.menu.start_has_active_test(),
                reply_markup=self._keyboards.start_has_active_test(),
            )
            return

        current_bot_name = await self._bot.get_my_name()

        await self._bot.send_message(
            chat_id=message.chat.id,
            text=self._strings.menu.start(
                bot_name=current_bot_name.name,
            ),
            reply_markup=self._keyboards.start(),
        )

    async def _export_handler(
            self,
            message: aiogram.types.Message,
            is_admin: bool,
    ) -> None:
        if not is_admin:
            await self._bot.send_message(
                chat_id=message.chat.id,
                text=self._strings.menu.export_unavailable(),
            )
            return

        current_users_list = self._database.users.get_users_list()

        current_users_data_frame = pandas.DataFrame(
            data=[
                [
                    user.id,
                    user.type.readable_name,
                    user.full_name,
                    user.phone_number,
                    user.email,
                    user.institution,
                    user.current_course,
                    user.recommended_course,
                    datetime.datetime.fromtimestamp(user.timestamp),
                ] for user in current_users_list
            ],
            columns=[
                "ID",
                "Статус",
                "ФИО",
                "Телефон",
                "Почта",
                "Учебное заведение",
                "Текущее направление",
                "Рекомендованное направление",
                "Время оставления заявки",
            ],
        )

        current_excel_file = io.BytesIO()
        with pandas.ExcelWriter(current_excel_file, engine="openpyxl") as writer:
            current_users_data_frame.to_excel(
                excel_writer=writer,
                index=False,
            )
        current_excel_file.seek(0)

        await self._bot.send_document(
            chat_id=message.chat.id,
            document=aiogram.types.BufferedInputFile(
                file=current_excel_file.read(),
                filename="ElkollegeGuidanceExport.xlsx",
            ),
        )

    async def _logs_handler(
            self,
            message: aiogram.types.Message,
            is_admin: bool,
    ) -> None:
        if not is_admin:
            return

        if not self._config.settings.file_logging:
            await self._bot.send_message(
                chat_id=message.chat.id,
                text=self._strings.menu.logging_disabled(),
            )
            return

        with self._logger.file as file:
            await self._bot.send_document(
                chat_id=message.chat.id,
                document=aiogram.types.BufferedInputFile(
                    file=file.read(),
                    filename=file.name,
                ),
            )

    # endregion
