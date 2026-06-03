import enum

import pydantic
import pyquoks.utils


class UserType(enum.IntEnum):
    SCHOOLKID = 0
    COLLEGE_STUDENT = 1
    UNIVERSITY_STUDENT = 2

    @property
    def readable_name(self) -> str:
        match self:
            case UserType.SCHOOLKID:
                return "Школьник"
            case UserType.COLLEGE_STUDENT:
                return "Студент СПО"
            case UserType.UNIVERSITY_STUDENT:
                return "Студент вуза"


class DatabaseUser(pydantic.BaseModel):
    id: int
    type: UserType
    full_name: str
    phone_number: str | None
    email: str | None
    institution: str
    current_course: str | None
    recommended_course: str
    timestamp: int


class CareerGuidanceTest(pydantic.BaseModel):
    professions: list[CareerGuidanceProfession]
    questions: list[CareerGuidanceQuestion]


class CareerGuidanceProfession(pydantic.BaseModel):
    id: int
    code: str
    name: str

    @property
    def text(self) -> str:
        return f"{self.code} {self.name}"


class CareerGuidanceQuestion(pydantic.BaseModel):
    question: str
    answers: list[CareerGuidanceAnswer]

    @property
    def text(self) -> str:
        return pyquoks.utils.format_multiline_string(
            """
            <b>{0}</b>
            
            {1}
            """,
            self.question,
            "\n".join(f"{index}. {answer.text}" for index, answer in enumerate(self.answers, start=1))
        )


class CareerGuidanceAnswer(pydantic.BaseModel):
    text: str
    profession_id: int
