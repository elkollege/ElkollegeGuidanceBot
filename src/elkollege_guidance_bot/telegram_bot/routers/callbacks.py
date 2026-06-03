import datetime
import typing

import aiogram
import aiogram.filters
import aiogram.fsm.context
import pyquoks.utils

from .. import states
from ..providers import keyboards
from ..services import logger
from ... import constants
from ... import models
from ...managers import database
from ...providers import guidance
from ...providers import strings


class CallbacksRouter(aiogram.Router):
    def __init__(
            self,
            database_manager: database.DatabaseManager,
            guidance_provider: guidance.GuidanceProvider,
            keyboards_provider: keyboards.KeyboardsProvider,
            strings_provider: strings.StringsProvider,
            logger_service: logger.LoggerService,
            aiogram_bot: aiogram.Bot,
    ) -> None:
        self._database = database_manager
        self._guidance = guidance_provider
        self._keyboards = keyboards_provider
        self._strings = strings_provider
        self._logger = logger_service
        self._bot = aiogram_bot

        super().__init__(
            name=self.__class__.__name__,
        )

        self.callback_query.outer_middleware.register(
            self._outer_middleware,
        )
        self.callback_query.register(
            self._callback_handler,
        )

        self._logger.info(f"{self.name} initialized!")

    # region Middlewares

    async def _outer_middleware(
            self,
            handler: typing.Callable[
                [
                    aiogram.types.CallbackQuery,
                    dict[str, typing.Any],
                ],
                typing.Awaitable[typing.Any],
            ],
            call: aiogram.types.CallbackQuery,
            data: dict[str, typing.Any],
    ) -> typing.Any:
        if call.data is None:
            return None

        state = data["raw_state"]

        self._logger.log_telegram_user_interaction(
            user=call.from_user,
            interaction=f"{call.data} ({state=})",
        )

        return await handler(call, data)

    # endregion

    # region Handlers

    async def _callback_handler(
            self,
            call: aiogram.types.CallbackQuery,
            state: aiogram.fsm.context.FSMContext,
    ) -> None:
        if call.data is None or call.message is None:
            return

        current_state = await state.get_state()

        try:
            match call.data.split(constants.CALL_DATA_SEPARATOR):
                case [
                    self._strings.callback.start,
                ]:
                    await state.clear()

                    current_bot_name = await self._bot.get_my_name()

                    await self._bot.edit_message_text(
                        chat_id=call.message.chat.id,
                        message_id=call.message.message_id,
                        text=self._strings.menu.start(
                            bot_name=current_bot_name.name,
                        ),
                        reply_markup=self._keyboards.start(),
                    )
                case [
                    self._strings.callback.user_type,
                    user_type,
                ] if current_state is None:
                    current_user_type = models.UserType(int(user_type))

                    await state.update_data(
                        data={
                            self._strings.state.current_user_type: current_user_type,
                        },
                    )
                    await state.set_state(states.Flow.personal_data_agreement)

                    await self._bot.edit_message_media(
                        chat_id=call.message.chat.id,
                        message_id=call.message.message_id,
                        media=aiogram.types.InputMediaDocument(
                            media=aiogram.types.FSInputFile(
                                path=pyquoks.utils.get_path("assets/personal_data_agreement.docx"),
                                filename="Согласие.docx",
                            ),
                            caption=self._strings.menu.personal_data_agreement(),
                        ),
                        reply_markup=self._keyboards.personal_data_agreement(),
                    )
                case [
                    self._strings.callback.personal_data_agreement,
                    agreement_status,
                ] if current_state == states.Flow.personal_data_agreement:
                    current_agreement_status = bool(int(agreement_status))

                    if not current_agreement_status:
                        await state.clear()

                        await self._bot.delete_message(
                            chat_id=call.message.chat.id,
                            message_id=call.message.message_id,
                        )
                        await self._bot.send_message(
                            chat_id=call.message.chat.id,
                            text=self._strings.menu.personal_data_agreement_disagree(),
                        )
                        return

                    await state.set_state(states.Flow.input_full_name)

                    await self._bot.edit_message_reply_markup(
                        chat_id=call.message.chat.id,
                        message_id=call.message.message_id,
                    )
                    await self._bot.send_message(
                        chat_id=call.message.chat.id,
                        text=self._strings.menu.input_full_name(),
                    )
                case [
                    self._strings.callback.answer,
                    question_index,
                    answer_index,
                ] if current_state == states.Flow.career_guidance_test:
                    current_question_index = int(question_index)
                    current_answer_index = int(answer_index)

                    current_question = self._guidance.test.questions[current_question_index]
                    current_answer = current_question.answers[current_answer_index]

                    # noinspection PyTypeChecker
                    current_profession_rating: dict = await state.get_value(
                        key=self._strings.state.professions_rating,
                        default={},
                    )
                    current_profession_id_rating = current_profession_rating.get(current_answer.profession_id, 0)
                    current_profession_rating.update(
                        {
                            current_answer.profession_id: current_profession_id_rating + 1,
                        }
                    )

                    await state.update_data(
                        data={
                            self._strings.state.professions_rating: current_profession_rating,
                        },
                    )

                    current_question_index += 1

                    if current_question_index < len(self._guidance.test.questions):
                        current_question = self._guidance.test.questions[current_question_index]

                        await self._bot.edit_message_text(
                            chat_id=call.message.chat.id,
                            message_id=call.message.message_id,
                            text=current_question.text,
                            reply_markup=self._keyboards.question_answers(
                                question_index=current_question_index,
                                answers=current_question.answers,
                            ),
                        )
                    else:
                        current_recommended_course = self._guidance.get_recommended_course(
                            professions_rating=current_profession_rating,
                        )

                        await state.update_data(
                            data={
                                self._strings.state.current_recommended_course: current_recommended_course.text,
                            },
                        )
                        await state.set_state(states.Flow.recommended_course_displayed)

                        await self._bot.edit_message_text(
                            chat_id=call.message.chat.id,
                            message_id=call.message.message_id,
                            text=self._strings.menu.recommended_course(
                                recommended_course=current_recommended_course,
                            ),
                            reply_markup=self._keyboards.recommended_course(),
                        )
                case [
                    self._strings.callback.leave_request,
                ] if current_state == states.Flow.recommended_course_displayed:
                    # noinspection PyTypeChecker
                    current_user_type: models.UserType = await state.get_value(
                        key=self._strings.state.current_user_type,
                    )
                    # noinspection PyTypeChecker
                    current_full_name: str = await state.get_value(
                        key=self._strings.state.current_full_name,
                    )
                    # noinspection PyTypeChecker
                    current_phone_number: str | None = await state.get_value(
                        key=self._strings.state.current_phone_number,
                    )
                    # noinspection PyTypeChecker
                    current_email: str | None = await state.get_value(
                        key=self._strings.state.current_email,
                    )
                    # noinspection PyTypeChecker
                    current_institution: str = await state.get_value(
                        key=self._strings.state.current_institution,
                    )
                    # noinspection PyTypeChecker
                    current_course: str | None = await state.get_value(
                        key=self._strings.state.current_course,
                    )
                    # noinspection PyTypeChecker
                    current_recommended_course: str = await state.get_value(
                        key=self._strings.state.current_recommended_course,
                    )

                    await state.clear()

                    self._database.users.add_user(
                        _type=current_user_type,
                        full_name=current_full_name,
                        phone_number=current_phone_number,
                        email=current_email,
                        institution=current_institution,
                        current_course=current_course,
                        recommended_course=current_recommended_course,
                        timestamp=int(datetime.datetime.now().timestamp()),
                    )

                    await self._bot.edit_message_reply_markup(
                        chat_id=call.message.chat.id,
                        message_id=call.message.message_id,
                    )
                    await self._bot.answer_callback_query(
                        callback_query_id=call.id,
                        text=self._strings.alert.request_submitted(),
                        show_alert=True,
                    )
                case _:
                    await self._bot.answer_callback_query(
                        callback_query_id=call.id,
                        text=self._strings.alert.button_unavailable(),
                        show_alert=True,
                    )
        except Exception as exception:
            if type(exception) in constants.AIOGRAM_IGNORED_EXCEPTIONS:
                return

            self._logger.log_exception(exception)
        finally:
            await self._bot.answer_callback_query(
                callback_query_id=call.id,
            )

    # endregion
