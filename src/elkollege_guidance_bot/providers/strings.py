import pyquoks.utils

from .. import models


class StringsProvider:
    alert: AlertStrings
    button: ButtonStrings
    callback: CallbackStrings
    menu: MenuStrings
    state: StateStrings

    def __init__(self) -> None:
        self.alert = AlertStrings()
        self.button = ButtonStrings()
        self.callback = CallbackStrings()
        self.menu = MenuStrings()
        self.state = StateStrings()


class AlertStrings:

    @classmethod
    def button_unavailable(cls) -> str:
        return "Данное тестирование недоступно, начните новое!"

    @classmethod
    def request_submitted(cls) -> str:
        return "Заявка оставлена!"


class ButtonStrings:

    # region /start

    @classmethod
    def start_new_test(cls) -> str:
        return "Начать новое тестирование"

    @classmethod
    def schoolkid(cls) -> str:
        return models.UserType.SCHOOLKID.readable_name

    @classmethod
    def college_student(cls) -> str:
        return models.UserType.COLLEGE_STUDENT.readable_name

    @classmethod
    def university_student(cls) -> str:
        return models.UserType.UNIVERSITY_STUDENT.readable_name

    @classmethod
    def agree(cls) -> str:
        return "Да"

    @classmethod
    def disagree(cls) -> str:
        return "Нет"

    @classmethod
    def answer(cls, answer_index: int) -> str:
        return f"{answer_index + 1}"

    @classmethod
    def leave_request(cls) -> str:
        return "Оставить заявку"

    # endregion


class CallbackStrings:

    # region /start

    @property
    def start(self) -> str:
        return "start"

    @property
    def user_type(self) -> str:
        return "user_type"

    @property
    def personal_data_agreement(self) -> str:
        return "personal_data_agreement"

    @property
    def answer(self) -> str:
        return "answer"

    @property
    def leave_request(self) -> str:
        return "leave_request"

    # endregion


class MenuStrings:

    # region /start

    @classmethod
    def start(cls, bot_name: str) -> str:
        return pyquoks.utils.format_multiline_string(
            """
            <b>Добро пожаловать в {0}!</b>
            Здесь вы можете пройти профориентационное тестирование и узнать, какое направление вам подойдёт!
            
            Выберите свой текущий статус:
            """,
            bot_name,
        )

    @classmethod
    def start_has_active_test(cls) -> str:
        return "У вас уже есть активное тестирование, хотите начать новое?"

    @classmethod
    def personal_data_agreement(cls) -> str:
        return "Продолжая, вы соглашаетесь с политикой обработки персональных данных."

    @classmethod
    def personal_data_agreement_disagree(cls) -> str:
        return "Спасибо за уделённое время!"

    @classmethod
    def input_full_name(cls) -> str:
        return "Введите своё полное ФИО:"

    @classmethod
    def input_phone_number(cls) -> str:
        return "Введите свой телефонный номер:"

    @classmethod
    def input_phone_number_error(cls) -> str:
        return pyquoks.utils.format_multiline_string(
            """
            <b>Некорректный формат!</b>
            Попробуйте ввести телефонный номер в следующем формате:
            <pre>+7(987)654-32-10</pre>
            
            {0}
            """,
            cls.input_phone_number()
        )

    @classmethod
    def input_email(cls) -> str:
        return "Введите свой адрес электронной почты:"

    @classmethod
    def input_email_error(cls) -> str:
        return pyquoks.utils.format_multiline_string(
            """
            <b>Некорректный формат!</b>
            Попробуйте ввести адрес электронной почты в следующем формате:
            <pre>email@example.com</pre>
            
            {0}
            """,
            cls.input_email()
        )

    @classmethod
    def input_institution(cls) -> str:
        return "Введите название своего текущего учебного заведения:"

    @classmethod
    def input_current_course(cls) -> str:
        return "Введите направление на котором сейчас обучаетесь:"

    @classmethod
    def recommended_course(cls, recommended_course: models.CareerGuidanceProfession) -> str:
        return pyquoks.utils.format_multiline_string(
            """
            <b>Тестирование окончено!</b>
            Ваше рекомендованное направление:
            {0}
            
            Если вы хотите получить консультацию по рекомендованному направлению, то вы можете оставить заявку по кнопке ниже.
            """,
            recommended_course.text,
        )

    # endregion

    # region /export

    @classmethod
    def export_unavailable(cls) -> str:
        return "Экспорт недоступен!"

    # endregion

    # region /logs

    @classmethod
    def logging_disabled(cls) -> str:
        return "Логирование отключено!"

    # endregion


class StateStrings:
    @property
    def current_user_type(self) -> str:
        return "current_user_type"

    @property
    def current_full_name(self) -> str:
        return "current_full_name"

    @property
    def current_phone_number(self) -> str:
        return "current_phone_number"

    @property
    def current_email(self) -> str:
        return "current_email"

    @property
    def current_institution(self) -> str:
        return "current_institution"

    @property
    def current_course(self) -> str:
        return "current_course"

    @property
    def current_recommended_course(self) -> str:
        return "current_recommended_course"

    @property
    def input_phone_number_retries_count(self) -> str:
        return "input_phone_number_retries_count"

    @property
    def input_email_retries_count(self) -> str:
        return "input_email_retries_count"

    @property
    def professions_rating(self) -> str:
        return "professions_rating"
