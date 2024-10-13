import re

from django.utils.deprecation import MiddlewareMixin
from django.conf import settings


class ReverseTextMiddleware(MiddlewareMixin):
    count_responses = 0

    def process_response(self, request, response):

        self.count_responses += 1
        self.count_responses %= 10

        if self.count_responses != 0 or not settings.ALLOW_REVERSE:
            return response

        content = response.content.decode("utf-8")

        def reverse_text(match):
            return match.group(1)[::-1]

        pattern = re.compile(r">([^<]+)<")
        reversed_content = re.sub(
            pattern, lambda m: f">{reverse_text(m)}<", content
        )

        if not re.search(r"<[^>]+>", content):
            reversed_content = content[::-1]

        response.content = reversed_content.encode("utf-8")

        return response
