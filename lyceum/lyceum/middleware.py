import re

from django.conf import settings


class ReverseWordsMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        self.count_responses = 0

    def __call__(self, request):
        response = self.get_response(request)
        self.count_responses += 1
        self.count_responses %= 10

        if self.count_responses != 0 or not settings.ALLOW_REVERSE:
            return response

        content = response.content.decode("utf-8")

        def reverse_word(word):
            return word[::-1]

        pattern = re.compile(r">([^<]+)<")

        def reverse_text_in_tag(match):
            text_inside_tags = match.group(1)
            words = text_inside_tags.split()
            reversed_words = [reverse_word(word) for word in words]
            return f">{' '.join(reversed_words)}<"

        reversed_content = re.sub(pattern, reverse_text_in_tag, content)

        if not re.search(r"<[^>]+>", content):
            words = content.split()
            reversed_content = " ".join(reverse_word(word) for word in words)

        response.content = reversed_content.encode("utf-8")

        return response
