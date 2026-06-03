import aiogram

from ... import constants
from ... import models
from ...providers import strings


class ButtonsProvider:
    def __init__(
            self,
            strings_provider: strings.StringsProvider,
    ) -> None:
        self._strings = strings_provider

    # region /start

    def start_new_test(self) -> aiogram.types.InlineKeyboardButton:
        return aiogram.types.InlineKeyboardButton(
            text=self._strings.button.start_new_test(),
            callback_data=self._strings.callback.start,
        )

    def schoolkid(self) -> aiogram.types.InlineKeyboardButton:
        return aiogram.types.InlineKeyboardButton(
            text=self._strings.button.schoolkid(),
            callback_data=constants.CALL_DATA_SEPARATOR.join([
                self._strings.callback.user_type,
                str(models.UserType.SCHOOLKID.value),
            ]),
        )

    def college_student(self) -> aiogram.types.InlineKeyboardButton:
        return aiogram.types.InlineKeyboardButton(
            text=self._strings.button.college_student(),
            callback_data=constants.CALL_DATA_SEPARATOR.join([
                self._strings.callback.user_type,
                str(models.UserType.COLLEGE_STUDENT.value),
            ]),
        )

    def university_student(self) -> aiogram.types.InlineKeyboardButton:
        return aiogram.types.InlineKeyboardButton(
            text=self._strings.button.university_student(),
            callback_data=constants.CALL_DATA_SEPARATOR.join([
                self._strings.callback.user_type,
                str(models.UserType.UNIVERSITY_STUDENT.value),
            ]),
        )

    def agree(self) -> aiogram.types.InlineKeyboardButton:
        return aiogram.types.InlineKeyboardButton(
            text=self._strings.button.agree(),
            callback_data=constants.CALL_DATA_SEPARATOR.join([
                self._strings.callback.personal_data_agreement,
                str(int(True)),
            ]),
        )

    def disagree(self) -> aiogram.types.InlineKeyboardButton:
        return aiogram.types.InlineKeyboardButton(
            text=self._strings.button.disagree(),
            callback_data=constants.CALL_DATA_SEPARATOR.join([
                self._strings.callback.personal_data_agreement,
                str(int(False)),
            ]),
        )

    def answer(self, question_index: int, answer_index: int) -> aiogram.types.InlineKeyboardButton:
        return aiogram.types.InlineKeyboardButton(
            text=self._strings.button.answer(
                answer_index=answer_index,
            ),
            callback_data=constants.CALL_DATA_SEPARATOR.join([
                self._strings.callback.answer,
                str(question_index),
                str(answer_index),
            ]),
        )

    def leave_request(self) -> aiogram.types.InlineKeyboardButton:
        return aiogram.types.InlineKeyboardButton(
            text=self._strings.button.leave_request(),
            callback_data=self._strings.callback.leave_request,
        )

    # endregion
