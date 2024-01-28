from rest_framework.exceptions import ValidationError


class URLValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        temp_val = dict(value).get(self.field)
        if "youtube.com" not in temp_val:
            raise ValidationError(f'URL-адрес запрещен')
