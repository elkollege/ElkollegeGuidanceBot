import typing

import aiogram
import aiogram.filters
import aiogram.fsm.context

from .. import states
from ..providers import keyboards
from ..services import logger
from ... import constants
from ... import models
from ... import utils
from ...managers import config
from ...providers import guidance
from ...providers import strings


class MessagesRouter(aiogram.Router):
    def __init__(
            self,
            config_manager: config.ConfigManager,
            guidance_provider: guidance.GuidanceProvider,
            keyboards_provider: keyboards.KeyboardsProvider,
            strings_provider: strings.StringsProvider,
            logger_service: logger.LoggerService,
            aiogram_bot: aiogram.Bot,
    ) -> None:
        self._config = config_manager
        self._guidance = guidance_provider
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
            self._personal_data_handler,
            aiogram.filters.StateFilter(
                states.Flow.input_full_name,
                states.Flow.input_phone_number,
                states.Flow.input_email,
                states.Flow.input_institution,
                states.Flow.input_current_course,
            ),
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
        if message.from_user is None:
            return None

        state = data["raw_state"]

        self._logger.log_telegram_user_interaction(
            user=message.from_user,
            interaction=f"{message.text} ({state=})",
        )

        return await handler(message, data)

    # endregion

    # region Handlers

    async def _personal_data_handler(
            self,
            message: aiogram.types.Message,
            state: aiogram.fsm.context.FSMContext,
    ) -> None:
        if message.text is None:
            return

        current_state = await state.get_state()

        match current_state:
            case states.Flow.input_full_name:
                await state.update_data(
                    data={
                        self._strings.state.current_full_name: message.text,
                    },
                )
                await state.set_state(states.Flow.input_phone_number)

                await self._bot.send_message(
                    chat_id=message.chat.id,
                    text=self._strings.menu.input_phone_number(),
                )
            case states.Flow.input_phone_number:
                if not utils.match_phone_number(message.text):
                    # noinspection PyTypeChecker
                    current_retries_count: int = await state.get_value(
                        key=self._strings.state.input_phone_number_retries_count,
                        default=constants.DEFAULT_MATCH_RETRIES_COUNT,
                    )

                    if current_retries_count < constants.MAX_MATCH_RETRIES_COUNT:
                        await state.update_data(
                            data={
                                self._strings.state.input_phone_number_retries_count: current_retries_count + 1,
                            },
                        )

                        await self._bot.send_message(
                            chat_id=message.chat.id,
                            text=self._strings.menu.input_phone_number_error(),
                        )
                        return

                    await state.update_data(
                        data={
                            self._strings.state.input_phone_number_retries_count: constants.DEFAULT_MATCH_RETRIES_COUNT,
                        },
                    )
                else:
                    await state.update_data(
                        data={
                            self._strings.state.current_phone_number: message.text,
                        },
                    )

                await state.set_state(states.Flow.input_email)

                await self._bot.send_message(
                    chat_id=message.chat.id,
                    text=self._strings.menu.input_email(),
                )
            case states.Flow.input_email:
                if not utils.match_email(message.text):
                    # noinspection PyTypeChecker
                    current_retries_count: int = await state.get_value(
                        key=self._strings.state.input_email_retries_count,
                        default=constants.DEFAULT_MATCH_RETRIES_COUNT,
                    )

                    if current_retries_count < constants.MAX_MATCH_RETRIES_COUNT:
                        await state.update_data(
                            data={
                                self._strings.state.input_email_retries_count: current_retries_count + 1,
                            },
                        )

                        await self._bot.send_message(
                            chat_id=message.chat.id,
                            text=self._strings.menu.input_email_error(),
                        )
                        return

                    await state.update_data(
                        data={
                            self._strings.state.input_email_retries_count: constants.DEFAULT_MATCH_RETRIES_COUNT,
                        },
                    )
                else:
                    await state.update_data(
                        data={
                            self._strings.state.current_email: message.text,
                        },
                    )

                await state.set_state(states.Flow.input_institution)

                await self._bot.send_message(
                    chat_id=message.chat.id,
                    text=self._strings.menu.input_institution(),
                )
            case states.Flow.input_institution:
                # noinspection PyTypeChecker
                current_user_type: models.UserType = await state.get_value(
                    key=self._strings.state.current_user_type,
                )

                await state.update_data(
                    data={
                        self._strings.state.current_institution: message.text,
                    },
                )

                if current_user_type == models.UserType.SCHOOLKID:
                    await self._send_first_career_guidance_question(
                        message=message,
                        state=state,
                    )
                else:
                    await state.set_state(states.Flow.input_current_course)

                    await self._bot.send_message(
                        chat_id=message.chat.id,
                        text=self._strings.menu.input_current_course(),
                    )
            case states.Flow.input_current_course:
                await state.update_data(
                    data={
                        self._strings.state.current_course: message.text,
                    },
                )

                await self._send_first_career_guidance_question(
                    message=message,
                    state=state,
                )

    # endregion

    # region Helpers

    async def _send_first_career_guidance_question(
            self,
            message: aiogram.types.Message,
            state: aiogram.fsm.context.FSMContext,
    ) -> None:
        current_question_index = constants.FIRST_CAREER_GUIDANCE_QUESTION_INDEX

        current_question = self._guidance.test.questions[current_question_index]

        await state.set_state(states.Flow.career_guidance_test)

        await self._bot.send_message(
            chat_id=message.chat.id,
            text=current_question.text,
            reply_markup=self._keyboards.question_answers(
                question_index=current_question_index,
                answers=current_question.answers,
            ),
        )

# endregion
