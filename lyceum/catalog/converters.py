class DigitConverter:
    regex = "[1-9]\\d*"

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return f"{value:d}"
