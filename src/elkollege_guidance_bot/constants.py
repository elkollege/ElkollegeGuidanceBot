import aiogram.exceptions

FIRST_CAREER_GUIDANCE_QUESTION_INDEX = 0

REGEX_PHONE_NUMBER = r"((8|\+7|\+38|\+374|\+375|\+380|\+993|\+994|\+995|\+996|\+998)[\- ]?)?\(?\d{3,5}\)?[\- ]?\d[\- ]?\d[\- ]?\d[\- ]?\d[\- ]?\d(([\- ]?\d)?[\- ]?\d)?"
REGEX_EMAIL = r"([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)"

DEFAULT_MATCH_RETRIES_COUNT = 0
MAX_MATCH_RETRIES_COUNT = 3

CALL_DATA_SEPARATOR = " "

AIOGRAM_IGNORED_EXCEPTIONS = (
    aiogram.exceptions.TelegramForbiddenError,
    aiogram.exceptions.TelegramRetryAfter,
)
