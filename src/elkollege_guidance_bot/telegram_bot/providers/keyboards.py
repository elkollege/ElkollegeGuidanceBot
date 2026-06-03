import aiogram
import aiogram.utils.keyboard

from . import buttons
from ... import models


class KeyboardsProvider:
    def __init__(
            self,
            buttons_provider: buttons.ButtonsProvider,
    ) -> None:
        self._buttons = buttons_provider

    # region /start

    def start(self) -> aiogram.types.InlineKeyboardMarkup:
        markup_builder = aiogram.utils.keyboard.InlineKeyboardBuilder()
        markup_builder.row(
            self._buttons.schoolkid(),
        )
        markup_builder.row(
            self._buttons.college_student(),
            self._buttons.university_student(),
        )

        return markup_builder.as_markup()

    def start_has_active_test(self) -> aiogram.types.InlineKeyboardMarkup:
        markup_builder = aiogram.utils.keyboard.InlineKeyboardBuilder()
        markup_builder.row(
            self._buttons.start_new_test(),
        )

        return markup_builder.as_markup()

    def personal_data_agreement(self) -> aiogram.types.InlineKeyboardMarkup:
        markup_builder = aiogram.utils.keyboard.InlineKeyboardBuilder()
        markup_builder.row(
            self._buttons.agree(),
            self._buttons.disagree(),
        )

        return markup_builder.as_markup()

    def question_answers(
            self,
            question_index: int,
            answers: list[models.CareerGuidanceAnswer],
    ) -> aiogram.types.InlineKeyboardMarkup:
        markup_builder = aiogram.utils.keyboard.InlineKeyboardBuilder()
        markup_builder.row(
            *[
                self._buttons.answer(
                    question_index=question_index,
                    answer_index=index,
                ) for index, answer in enumerate(answers)
            ],
        )

        return markup_builder.as_markup()

    def recommended_course(self) -> aiogram.types.InlineKeyboardMarkup:
        markup_builder = aiogram.utils.keyboard.InlineKeyboardBuilder()
        markup_builder.row(
            self._buttons.leave_request(),
        )

        return markup_builder.as_markup()

    # endregion
