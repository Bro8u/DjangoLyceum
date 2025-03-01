__all__ = ["DigitConverter"]


class DigitConverter:
    regex = r"0*[1-9]{1,}\d*"

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return f"{value:d}"
