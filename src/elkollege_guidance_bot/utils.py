import re

from . import constants


def match_phone_number(string: str) -> bool:
    if not bool(re.fullmatch(constants.REGEX_PHONE_NUMBER, string)):
        return False

    code_chunk = re.split(constants.REGEX_PHONE_NUMBER, string)[2]

    if code_chunk is None:
        return False

    string_without_code_chunk = string.replace(code_chunk, "", 1)

    return len(re.findall(r"\d", string_without_code_chunk)) == 10


def match_email(string: str) -> bool:
    return bool(re.fullmatch(constants.REGEX_EMAIL, string))
