class DigitConverter:
    regex = "[0-9]\\d*"

    def to_python(self, value):
        if int(value) == 0:
            raise ValueError("только из нули")
        return int(value)

    def to_url(self, value):
        return f"{value:d}"
