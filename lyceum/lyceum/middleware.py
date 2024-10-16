import re

from django.conf import settings


class ReverseWordsMiddleware:
    count_responses = 0

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if not settings.ALLOW_REVERSE:
            return response

        ReverseWordsMiddleware.count_responses += 1

        if ReverseWordsMiddleware.count_responses % 10 != 0:
            return response

        ReverseWordsMiddleware.count_responses = 0

        content = response.content.decode("utf-8")
        reversed_content = reverse_cyrillic_words(content)

        response.content = reversed_content.encode("utf-8")
        return response


def reverse_word(word):
    return word[::-1]


def reverse_cyrillic_words(text):
    pattern = re.compile(r"\b[а-яА-ЯёЁ]+\b")

    def replace(match):
        return reverse_word(match.group(0))

    return pattern.sub(replace, text)
