import re

from django.core.exceptions import ValidationError


WORDS_REGEX = re.compile(r"\w+|\W+")


def validate_text(value):
    words = set(WORDS_REGEX.findall(value.lower()))
    if not {"превосходно", "роскошно"} & words:
        raise ValidationError(
            'В тексте должно быть слово "превосходно" или "роскошно".'
        )
